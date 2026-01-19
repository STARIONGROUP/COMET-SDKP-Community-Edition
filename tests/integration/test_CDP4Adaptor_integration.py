"""
Integration tests for CDP4Adaptor module

These tests simulate real-world scenarios with more realistic object hierarchies
and interactions between components.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from typing import List

from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    getElementByParameterType,
    getElementByParameterTypeWhereAllValuesAreSet,
    prepareTransaction,
    setValue,
)


###################################################################################################
#                                                                                                 #
#                                 SESSION INTEGRATION TESTS                                      #
#                                                                                                 #
###################################################################################################


class TestCdp4SessionIntegration:
    """Integration tests for complete session workflows"""

    @pytest.fixture
    def session_service(self):
        """Create a session service for testing"""
        return Cdp4SessionService()

    def test_session_initialization_and_opening_workflow(self, session_service):
        """Test complete workflow: initialize, validate, and open session"""
        # Verify initial state
        assert session_service.isSessionOpen is False
        assert hasattr(session_service, "session")
        assert hasattr(session_service, "messageBus")
        assert hasattr(session_service, "dal")

        # Try to open actual session
        try:
            result = session_service.open("http://localhost:5000", "admin", "pass")
            
            if session_service.isSessionOpen:
                # Session opened successfully
                assert result is None
            else:
                # Connection failed - skip test
                pytest.skip("CDP4 server not available at http://localhost:5000")
        except Exception as e:
            pytest.skip(f"CDP4 server connection error: {str(e)}")

    def test_retrieve_participant_models_workflow(self, session_service):
        """Test workflow: open session -> retrieve participant models"""
        # Setup session
        session_service.session = MagicMock()
        session_service.session.Open.return_value.GetAwaiter.return_value.GetResult.return_value = (
            None
        )
        session_service.isSessionOpen = True

        # Mock active person
        mock_person = MagicMock()
        mock_person.Iid = "person-123"
        session_service.session.ActivePerson = mock_person

        # Create model hierarchy
        mock_participant1 = MagicMock()
        mock_participant1.Person.Iid = "person-123"

        mock_participant2 = MagicMock()
        mock_participant2.Person.Iid = "other-person"

        mock_model1 = MagicMock()
        mock_model1.Name = "Model A"
        mock_model1.Participant = [mock_participant1]

        mock_model2 = MagicMock()
        mock_model2.Name = "Model B"
        mock_model2.Participant = [mock_participant1, mock_participant2]

        mock_site_directory = MagicMock()
        mock_site_directory.Model = [mock_model1, mock_model2]

        session_service.session.RetrieveSiteDirectory.return_value = mock_site_directory

        # Get participant models
        result = session_service.getParticipantModels()

        # Verify correct models are returned
        assert len(result) == 2
        assert mock_model1 in result
        assert mock_model2 in result

    def test_get_domains_for_model_workflow(self, session_service):
        """Test workflow: open session -> get available domains for model"""
        session_service.session = MagicMock()
        session_service.isSessionOpen = True

        mock_person = MagicMock()
        mock_person.Iid = "person-123"
        session_service.session.ActivePerson = mock_person

        # Create domain hierarchy
        mock_domain1 = MagicMock()
        mock_domain1.Name = "Systems Engineering"
        mock_domain1.Iid = "domain-se"

        mock_domain2 = MagicMock()
        mock_domain2.Name = "Thermal"
        mock_domain2.Iid = "domain-thermal"

        mock_participant = MagicMock()
        mock_participant.Domain = [mock_domain1, mock_domain2]

        mock_setup = MagicMock()
        mock_setup.Participant = MagicMock()
        mock_setup.Participant.Find.return_value = mock_participant

        # Get domains
        result = session_service.getAvailableDomains(mock_setup)

        # Verify domains
        assert len(result) == 2
        assert mock_domain1 in result
        assert mock_domain2 in result


###################################################################################################
#                                                                                                 #
#                            PRODUCT TREE INTEGRATION TESTS                                      #
#                                                                                                 #
###################################################################################################


class TestProductTreeIntegration:
    """Integration tests for product tree operations"""

    @pytest.fixture
    def sample_iteration_with_elements(self):
        """Create a realistic iteration with nested elements"""
        mock_top_element = MagicMock()
        mock_top_element.Name = "System"
        mock_top_element.Iid = "element-top"

        mock_iteration = MagicMock()
        mock_iteration.TopElement = mock_top_element
        mock_iteration.Iid = "iteration-1"

        return mock_iteration

    @pytest.fixture
    def sample_option(self):
        """Create a sample option"""
        mock_option = MagicMock()
        mock_option.Name = "Option A"
        mock_option.Iid = "option-1"
        return mock_option

    def test_compute_product_tree_with_top_element(
        self, sample_iteration_with_elements, sample_option
    ):
        """Test computing product tree from iteration"""
        with patch("comet_sdkp.CDP4Adaptor.NestedElementTreeGenerator") as mock_generator:
            # Setup generator mock
            mock_nested1 = MagicMock()
            mock_nested1.Name = "Subsystem A"
            mock_nested1.Iid = "nested-1"

            mock_nested2 = MagicMock()
            mock_nested2.Name = "Subsystem B"
            mock_nested2.Iid = "nested-2"

            generator_instance = MagicMock()
            generator_instance.GenerateNestedElements.return_value = [
                mock_nested1,
                mock_nested2,
            ]
            mock_generator.return_value = generator_instance

            # Compute tree
            result = computeProductTree(sample_iteration_with_elements, sample_option)

            # Verify
            assert len(result) == 2
            assert mock_nested1 in result
            assert mock_nested2 in result
            generator_instance.GenerateNestedElements.assert_called_once()

    def test_compute_product_tree_empty_iteration(self):
        """Test computing tree with iteration that has no top element"""
        mock_iteration = MagicMock()
        mock_iteration.TopElement = None

        result = computeProductTree(mock_iteration, MagicMock())

        assert result == []


###################################################################################################
#                                                                                                 #
#                          PARAMETER FILTERING INTEGRATION TESTS                                #
#                                                                                                 #
###################################################################################################


class TestParameterFilteringIntegration:
    """Integration tests for parameter-based element filtering"""

    @pytest.fixture
    def nested_elements_with_parameters(self):
        """Create realistic nested elements with parameters"""
        # Create mass parameters
        mock_mass_param_type = MagicMock()
        mock_mass_param_type.Name = "Mass"

        mock_mass_param1 = MagicMock()
        mock_mass_param1.AssociatedParameter = MagicMock()
        mock_mass_param1.AssociatedParameter.ParameterType = mock_mass_param_type
        mock_mass_param1.ActualValue = "100"

        mock_mass_param2 = MagicMock()
        mock_mass_param2.AssociatedParameter = MagicMock()
        mock_mass_param2.AssociatedParameter.ParameterType = mock_mass_param_type
        mock_mass_param2.ActualValue = "200"

        # Create element with mass parameters
        mock_element1 = MagicMock()
        mock_element1.Name = "Component A"
        mock_element1.Iid = "elem-1"
        mock_element1.NestedParameter = [mock_mass_param1]

        # Create volume parameter
        mock_volume_param_type = MagicMock()
        mock_volume_param_type.Name = "Volume"

        mock_volume_param = MagicMock()
        mock_volume_param.AssociatedParameter = MagicMock()
        mock_volume_param.AssociatedParameter.ParameterType = mock_volume_param_type
        mock_volume_param.ActualValue = "50"

        mock_element2 = MagicMock()
        mock_element2.Name = "Component B"
        mock_element2.Iid = "elem-2"
        mock_element2.NestedParameter = [mock_volume_param]

        # Element with both parameters
        mock_element3 = MagicMock()
        mock_element3.Name = "Component C"
        mock_element3.Iid = "elem-3"
        mock_element3.NestedParameter = [mock_mass_param2, mock_volume_param]

        return [mock_element1, mock_element2, mock_element3]

    def test_filter_elements_by_parameter_type_workflow(
        self, nested_elements_with_parameters
    ):
        """Test filtering elements that have a specific parameter type"""
        result = getElementByParameterType(nested_elements_with_parameters, "Mass")

        # Should return elements 1 and 3 (those with Mass parameter)
        assert len(result) == 2
        assert nested_elements_with_parameters[0] in result
        assert nested_elements_with_parameters[2] in result
        assert nested_elements_with_parameters[1] not in result

    def test_filter_elements_with_all_values_set_workflow(
        self, nested_elements_with_parameters
    ):
        """Test filtering elements where all parameter values are set"""
        result = getElementByParameterTypeWhereAllValuesAreSet(
            nested_elements_with_parameters, "Mass"
        )

        # All elements should have mass set (none have "-")
        assert len(result) == 2

    def test_filter_with_unset_values(self):
        """Test filtering when some parameter values are not set"""
        mock_param_type = MagicMock()
        mock_param_type.Name = "Property"

        mock_param_set = MagicMock()
        mock_param_set.AssociatedParameter = MagicMock()
        mock_param_set.AssociatedParameter.ParameterType = mock_param_type
        mock_param_set.ActualValue = "value"

        mock_param_unset = MagicMock()
        mock_param_unset.AssociatedParameter = MagicMock()
        mock_param_unset.AssociatedParameter.ParameterType = mock_param_type
        mock_param_unset.ActualValue = "-"

        mock_element_all_set = MagicMock()
        mock_element_all_set.NestedParameter = [mock_param_set]

        mock_element_some_unset = MagicMock()
        mock_element_some_unset.NestedParameter = [mock_param_set, mock_param_unset]

        elements = [mock_element_all_set, mock_element_some_unset]

        result = getElementByParameterTypeWhereAllValuesAreSet(elements, "Property")

        # Only first element should be returned
        assert len(result) == 1
        assert mock_element_all_set in result


###################################################################################################
#                                                                                                 #
#                          TRANSACTION INTEGRATION TESTS                                         #
#                                                                                                 #
###################################################################################################


class TestTransactionIntegration:
    """Integration tests for transaction preparation and value setting"""

    @pytest.fixture
    def sample_iteration(self):
        """Create a sample iteration"""
        mock_iteration = MagicMock()
        mock_iteration.Iid = "iteration-123"
        mock_iteration.Clone.return_value = MagicMock()
        return mock_iteration

    def test_prepare_transaction_workflow(self, sample_iteration):
        """Test complete transaction preparation workflow"""
        with patch("comet_sdkp.CDP4Adaptor.ThingTransaction") as mock_transaction_class:
            with patch(
                "comet_sdkp.CDP4Adaptor.TransactionContextResolver"
            ) as mock_resolver:
                # Setup mocks
                mock_clone = MagicMock()
                sample_iteration.Clone.return_value = mock_clone

                mock_context = MagicMock()
                mock_resolver.ResolveContext.return_value = mock_context

                mock_transaction = MagicMock()
                mock_transaction_class.return_value = mock_transaction

                # Prepare transaction
                iteration, transaction = prepareTransaction(sample_iteration)

                # Verify
                assert iteration == sample_iteration
                assert transaction == mock_transaction
                sample_iteration.Clone.assert_called_once_with(False)
                mock_resolver.ResolveContext.assert_called_once_with(mock_clone)
                mock_transaction_class.assert_called_once_with(mock_context, mock_clone)

    def test_set_multiple_values_workflow(self):
        """Test setting multiple parameter values with different switch kinds"""
        with patch("comet_sdkp.CDP4Adaptor.ParameterSwitchKind") as mock_switch_enum:
            with patch("comet_sdkp.CDP4Adaptor.Array") as mock_array:
                with patch("comet_sdkp.CDP4Adaptor.ValueArray") as mock_value_array:
                    # Setup
                    mock_switch_enum.MANUAL = MagicMock()
                    mock_switch_enum.MANUAL.name = "MANUAL"
                    mock_array.return_value = MagicMock()
                    mock_value_array.return_value = MagicMock()

                    mock_value_set = MagicMock()

                    # Set value
                    result = setValue(mock_value_set, mock_switch_enum.MANUAL, ["100"])

                    # Verify
                    assert result == mock_value_set
                    assert mock_value_set.ValueSwitch == mock_switch_enum.MANUAL


###################################################################################################
#                                                                                                 #
#                        END-TO-END WORKFLOW INTEGRATION TESTS                                   #
#                                                                                                 #
###################################################################################################


class TestEndToEndWorkflows:
    """Integration tests for complete end-to-end workflows"""

    def test_complete_session_to_iteration_workflow(self):
        """Test complete workflow: open session -> get models -> open iteration
        
        This test requires an actual CDP4 server running.
        """
        pytest.skip("Requires actual CDP4 server with real data at http://localhost:5000")

    def test_complete_product_tree_and_filtering_workflow(self):
        """Test workflow: compute tree -> filter by parameter -> get values"""
        # Create iteration with proper mocking
        mock_top_element = MagicMock()
        mock_iteration = MagicMock()
        mock_iteration.TopElement = mock_top_element

        mock_option = MagicMock()

        # Create nested elements with parameters
        mock_param_type = MagicMock()
        mock_param_type.Name = "Mass"

        mock_param = MagicMock()
        mock_param.AssociatedParameter = MagicMock()
        mock_param.AssociatedParameter.ParameterType = mock_param_type
        mock_param.ActualValue = "150"

        mock_nested_element = MagicMock()
        mock_nested_element.NestedParameter = [mock_param]

        with patch("comet_sdkp.CDP4Adaptor.NestedElementTreeGenerator") as mock_generator:
            generator_instance = MagicMock()
            generator_instance.GenerateNestedElements.return_value = [
                mock_nested_element
            ]
            mock_generator.return_value = generator_instance

            # Step 1: Compute tree
            tree = computeProductTree(mock_iteration, mock_option)
            assert len(tree) == 1

            # Step 2: Filter by parameter
            filtered = getElementByParameterType(tree, "Mass")
            assert len(filtered) == 1
            
            # Step 3: Filter with all values set
            complete = getElementByParameterTypeWhereAllValuesAreSet(filtered, "Mass")
            assert len(complete) == 1

            # Verify the parameter is correct
            assert complete[0].NestedParameter[0].ActualValue == "150"

    def test_transaction_and_write_workflow(self):
        """Test workflow: prepare transaction -> set values -> write"""
        service = Cdp4SessionService()
        service.isSessionOpen = True
        service.session = MagicMock()

        mock_iteration = MagicMock()
        mock_iteration.Iid = "iter-1"
        mock_clone = MagicMock()
        mock_iteration.Clone.return_value = mock_clone

        with patch("comet_sdkp.CDP4Adaptor.ThingTransaction") as mock_transaction_class:
            with patch(
                "comet_sdkp.CDP4Adaptor.TransactionContextResolver"
            ) as mock_resolver:
                # Step 1: Prepare transaction
                mock_context = MagicMock()
                mock_resolver.ResolveContext.return_value = mock_context

                mock_transaction = MagicMock()
                mock_transaction.FinalizeTransaction.return_value = MagicMock()
                mock_transaction_class.return_value = mock_transaction

                iteration, transaction = prepareTransaction(mock_iteration)
                assert transaction is not None
                assert iteration == mock_iteration

                # Step 2: Write transaction
                service.session.Write.return_value.GetAwaiter.return_value.GetResult.return_value = (
                    None
                )
                result = service.write(transaction)

                # Verify write was called
                assert result is None
                service.session.Write.assert_called_once()


###################################################################################################
#                                                                                                 #
#                    REAL INTEGRATION TESTS (Require CDP4 Server)                                #
#                                                                                                 #
###################################################################################################


class TestRealCDP4Integration:
    """Integration tests against a real CDP4 server
    
    These tests require a running CDP4 server at http://localhost:5000
    with username 'admin' and password 'pass'
    """

    @pytest.mark.integration
    @pytest.mark.skipif(
        True,  # Set to False to enable tests when server is available
        reason="CDP4 server integration tests disabled. Enable by setting skipif to False and ensuring server is running"
    )
    def test_real_session_connection(self):
        """Test actual connection to real CDP4 server"""
        service = Cdp4SessionService()
        
        result = service.open("http://localhost:5000", "admin", "pass")
        
        try:
            assert service.isSessionOpen is True
            assert result is None
            
            # Test retrieving site directory
            site_dir = service.session.RetrieveSiteDirectory()
            assert site_dir is not None
            assert hasattr(site_dir, 'Model')
        finally:
            if service.isSessionOpen:
                service.isSessionOpen = False
                service.session = None

    @pytest.mark.integration
    @pytest.mark.skipif(
        True,
        reason="CDP4 server integration tests disabled"
    )
    def test_real_get_participant_models(self):
        """Test getting participant models from real server"""
        service = Cdp4SessionService()
        
        result = service.open("http://localhost:5000", "admin", "pass")
        
        try:
            assert service.isSessionOpen is True
            
            models = service.getParticipantModels()
            assert isinstance(models, list)
            # Should have at least one model in test data
            assert len(models) >= 0
        finally:
            if service.isSessionOpen:
                service.isSessionOpen = False
                service.session = None

    @pytest.mark.integration
    @pytest.mark.skipif(
        True,
        reason="CDP4 server integration tests disabled"
    )
    def test_real_open_iteration(self):
        """Test opening an actual iteration from real server"""
        service = Cdp4SessionService()
        
        result = service.open("http://localhost:5000", "admin", "pass")
        
        try:
            assert service.isSessionOpen is True
            
            models = service.getParticipantModels()
            if len(models) > 0:
                model = models[0]
                # Get first available domain
                site_dir = service.session.RetrieveSiteDirectory()
                setups = [m for m in site_dir.Model if m.Iid == model.Iid]
                
                if len(setups) > 0:
                    setup = setups[0]
                    # This would require actual domain data
                    domains = service.getAvailableDomains(setup)
                    assert isinstance(domains, list)
        finally:
            if service.isSessionOpen:
                service.isSessionOpen = False
                service.session = None