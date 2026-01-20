"""
Integration tests for CDP4Adaptor module

These tests simulate real-world scenarios with more realistic object hierarchies
and interactions between components.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from typing import List
import sys

# Mock CDP4 modules
sys.modules["clr"] = MagicMock()
sys.modules["System"] = MagicMock()
sys.modules["System.Threading"] = MagicMock()
sys.modules["CDP4Common"] = MagicMock()
sys.modules["CDP4Common.Helpers"] = MagicMock()
sys.modules["CDP4Common.EngineeringModelData"] = MagicMock()
sys.modules["CDP4Common.SiteDirectoryData"] = MagicMock()
sys.modules["CDP4Common.Types"] = MagicMock()
sys.modules["CDP4Dal"] = MagicMock()
sys.modules["CDP4Dal.DAL"] = MagicMock()
sys.modules["CDP4Dal.Operations"] = MagicMock()
sys.modules["CDP4ServicesDal"] = MagicMock()

from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    getElementByParameterType,
    getElementByParameterTypeWhereAllValuesAreSet,
    prepareTransaction,
    setValue,
    InvalidParametersException,
    SessionException,
)


###################################################################################################
#                                         FIXTURES                                                #
###################################################################################################


@pytest.fixture
def mock_session_service():
    """Provides a Cdp4SessionService instance for integration testing"""
    service = Cdp4SessionService()
    return service


@pytest.fixture
def mock_site_directory():
    """Create a realistic site directory structure"""
    mock_site_dir = MagicMock()
    mock_site_dir.Model = []
    return mock_site_dir


@pytest.fixture
def mock_person():
    """Create a mock person/user"""
    person = MagicMock()
    person.Iid = "person-123"
    person.Name = "Test User"
    return person


@pytest.fixture
def mock_domain():
    """Create a mock domain of expertise"""
    domain = MagicMock()
    domain.Name = "Systems Engineering"
    domain.Iid = "domain-se-001"
    return domain


@pytest.fixture
def mock_iteration():
    """Create a mock iteration"""
    iteration = MagicMock()
    iteration.Iid = "iteration-001"
    iteration.TopElement = MagicMock()
    iteration.TopElement.Name = "System"
    iteration.Option = []
    return iteration


@pytest.fixture
def mock_option():
    """Create a mock option"""
    option = MagicMock()
    option.Name = "Option A"
    option.Iid = "option-001"
    return option


###################################################################################################
#                                   SESSION INTEGRATION TESTS                                    #
###################################################################################################


class TestCdp4SessionIntegration:
    """Integration tests for complete session workflows"""

    def test_session_initialization_and_properties(self, mock_session_service):
        """Test session initialization and basic properties"""
        # Verify initial state
        assert mock_session_service.isSessionOpen is False
        assert mock_session_service.session is None
        assert hasattr(mock_session_service, "messageBus")
        assert hasattr(mock_session_service, "dal")
        assert mock_session_service.messageBus is not None
        assert mock_session_service.dal is not None

    def test_session_open_close_cycle(self, mock_session_service):
        """Test opening and closing a session"""
        # Mock the session
        mock_session_service.session = MagicMock()
        mock_session_service.session.Close.return_value.GetAwaiter.return_value.GetResult.return_value = (
            None
        )
        mock_session_service.isSessionOpen = True

        # Close the session
        result = mock_session_service.close()

        # Verify closure
        assert result is None
        assert mock_session_service.isSessionOpen is False
        assert mock_session_service.session is None

    def test_retrieve_participant_models_workflow(self, mock_session_service, mock_person):
        """Test workflow: open session -> retrieve participant models"""
        # Setup session
        mock_session_service.session = MagicMock()
        mock_session_service.session.Open.return_value.GetAwaiter.return_value.GetResult.return_value = (
            None
        )
        mock_session_service.isSessionOpen = True
        mock_session_service.session.ActivePerson = mock_person

        # Create model hierarchy
        mock_participant1 = MagicMock()
        mock_participant1.Person.Iid = "person-123"

        mock_participant2 = MagicMock()
        mock_participant2.Person.Iid = "other-person"

        mock_model1 = MagicMock()
        mock_model1.Name = "Model A"
        mock_model1.Iid = "model-001"
        mock_model1.Participant = [mock_participant1]

        mock_model2 = MagicMock()
        mock_model2.Name = "Model B"
        mock_model2.Iid = "model-002"
        mock_model2.Participant = [mock_participant1, mock_participant2]

        mock_site_directory = MagicMock()
        mock_site_directory.Model = [mock_model1, mock_model2]

        mock_session_service.session.RetrieveSiteDirectory.return_value = mock_site_directory

        # Get participant models
        result = mock_session_service.getParticipantModels()

        # Verify correct models are returned
        assert len(result) == 2
        assert mock_model1 in result
        assert mock_model2 in result

    def test_retrieve_models_user_not_participant(self, mock_session_service, mock_person):
        """Test retrieving models when user is not a participant"""
        # Setup session
        mock_session_service.session = MagicMock()
        mock_session_service.isSessionOpen = True
        mock_session_service.session.ActivePerson = mock_person

        # Create models where user is NOT a participant
        mock_other_person = MagicMock()
        mock_other_person.Iid = "other-person"

        mock_participant = MagicMock()
        mock_participant.Person.Iid = "other-person"

        mock_model = MagicMock()
        mock_model.Name = "Model A"
        mock_model.Participant = [mock_participant]

        mock_site_directory = MagicMock()
        mock_site_directory.Model = [mock_model]

        mock_session_service.session.RetrieveSiteDirectory.return_value = mock_site_directory

        # Get participant models
        result = mock_session_service.getParticipantModels()

        # Should return empty list
        assert result == []

    def test_get_domains_for_model_workflow(self, mock_session_service, mock_person, mock_domain):
        """Test workflow: open session -> get available domains for model"""
        mock_session_service.session = MagicMock()
        mock_session_service.isSessionOpen = True
        mock_session_service.session.ActivePerson = mock_person

        # Create domain hierarchy
        mock_domain2 = MagicMock()
        mock_domain2.Name = "Thermal"
        mock_domain2.Iid = "domain-thermal"

        mock_participant = MagicMock()
        mock_participant.Domain = [mock_domain, mock_domain2]

        mock_setup = MagicMock()
        mock_setup.Name = "TestModel"
        mock_setup.Participant = MagicMock()
        mock_setup.Participant.Find.return_value = mock_participant

        # Get domains
        result = mock_session_service.getAvailableDomains(mock_setup)

        # Verify domains
        assert len(result) == 2
        assert mock_domain in result
        assert mock_domain2 in result

    def test_get_domains_when_user_not_participant(self, mock_session_service):
        """Test getting domains when user is not a participant"""
        mock_session_service.session = MagicMock()
        mock_session_service.isSessionOpen = True

        mock_setup = MagicMock()
        mock_setup.Participant = MagicMock()
        mock_setup.Participant.Find.return_value = None

        result = mock_session_service.getAvailableDomains(mock_setup)

        assert result == []


###################################################################################################
#                               PRODUCT TREE INTEGRATION TESTS                                   #
###################################################################################################


class TestProductTreeIntegration:
    """Integration tests for product tree operations"""

    def test_compute_product_tree_with_hierarchy(self, mock_iteration, mock_option):
        """Test computing product tree with realistic hierarchy"""
        with patch("comet_sdkp.CDP4Adaptor.NestedElementTreeGenerator") as mock_generator:
            # Create realistic nested elements
            mock_subsystem_a = MagicMock()
            mock_subsystem_a.Name = "Subsystem A"
            mock_subsystem_a.Iid = "nested-001"
            mock_subsystem_a.NestedParameter = []

            mock_subsystem_b = MagicMock()
            mock_subsystem_b.Name = "Subsystem B"
            mock_subsystem_b.Iid = "nested-002"
            mock_subsystem_b.NestedParameter = []

            generator_instance = MagicMock()
            generator_instance.GenerateNestedElements.return_value = [
                mock_subsystem_a,
                mock_subsystem_b,
            ]
            mock_generator.return_value = generator_instance

            # Compute tree
            result = computeProductTree(mock_iteration, mock_option)

            # Verify
            assert len(result) == 2
            assert mock_subsystem_a in result
            assert mock_subsystem_b in result
            generator_instance.GenerateNestedElements.assert_called_once()

    def test_compute_product_tree_single_element(self, mock_iteration, mock_option):
        """Test computing tree with single element"""
        with patch("comet_sdkp.CDP4Adaptor.NestedElementTreeGenerator") as mock_generator:
            mock_element = MagicMock()
            mock_element.Name = "SingleElement"
            mock_element.Iid = "elem-001"

            generator_instance = MagicMock()
            generator_instance.GenerateNestedElements.return_value = [mock_element]
            mock_generator.return_value = generator_instance

            result = computeProductTree(mock_iteration, mock_option)

            assert len(result) == 1
            assert mock_element in result

    def test_compute_product_tree_empty(self, mock_iteration, mock_option):
        """Test computing tree with empty result"""
        with patch("comet_sdkp.CDP4Adaptor.NestedElementTreeGenerator") as mock_generator:
            generator_instance = MagicMock()
            generator_instance.GenerateNestedElements.return_value = []
            mock_generator.return_value = generator_instance

            result = computeProductTree(mock_iteration, mock_option)

            assert result == []

    def test_compute_product_tree_invalid_inputs(self):
        """Test computing tree with invalid inputs"""
        # Test with None iteration
        with pytest.raises(InvalidParametersException):
            computeProductTree(None, MagicMock())

        # Test with None option
        with pytest.raises(InvalidParametersException):
            computeProductTree(MagicMock(), None)

    def test_compute_product_tree_no_top_element(self, mock_option):
        """Test computing tree when iteration has no top element"""
        mock_iteration = MagicMock()
        mock_iteration.TopElement = None

        result = computeProductTree(mock_iteration, mock_option)

        assert result == []


###################################################################################################
#                           PARAMETER FILTERING INTEGRATION TESTS                               #
###################################################################################################


class TestParameterFilteringIntegration:
    """Integration tests for parameter-based element filtering"""

    @pytest.fixture
    def nested_elements_with_parameters(self):
        """Create realistic nested elements with multiple parameters"""
        # Create mass parameter type and values
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

        # Element with mass parameter
        mock_element1 = MagicMock()
        mock_element1.Name = "Component A"
        mock_element1.Iid = "elem-001"
        mock_element1.NestedParameter = [mock_mass_param1]

        # Create volume parameter type
        mock_volume_param_type = MagicMock()
        mock_volume_param_type.Name = "Volume"

        mock_volume_param = MagicMock()
        mock_volume_param.AssociatedParameter = MagicMock()
        mock_volume_param.AssociatedParameter.ParameterType = mock_volume_param_type
        mock_volume_param.ActualValue = "50"

        # Element with volume parameter
        mock_element2 = MagicMock()
        mock_element2.Name = "Component B"
        mock_element2.Iid = "elem-002"
        mock_element2.NestedParameter = [mock_volume_param]

        # Element with both parameters
        mock_element3 = MagicMock()
        mock_element3.Name = "Component C"
        mock_element3.Iid = "elem-003"
        mock_element3.NestedParameter = [mock_mass_param2, mock_volume_param]

        return [mock_element1, mock_element2, mock_element3]

    def test_filter_elements_by_parameter_type(self, nested_elements_with_parameters):
        """Test filtering elements by parameter type"""
        result = getElementByParameterType(nested_elements_with_parameters, "Mass")

        # Should return elements with Mass parameter (0 and 2)
        assert len(result) == 2
        assert nested_elements_with_parameters[0] in result
        assert nested_elements_with_parameters[2] in result
        assert nested_elements_with_parameters[1] not in result

    def test_filter_elements_by_different_parameter_type(self, nested_elements_with_parameters):
        """Test filtering by different parameter type"""
        result = getElementByParameterType(nested_elements_with_parameters, "Volume")

        # Should return elements with Volume parameter (1 and 2)
        assert len(result) == 2
        assert nested_elements_with_parameters[1] in result
        assert nested_elements_with_parameters[2] in result
        assert nested_elements_with_parameters[0] not in result

    def test_filter_elements_no_matches(self, nested_elements_with_parameters):
        """Test filtering when no elements match"""
        result = getElementByParameterType(nested_elements_with_parameters, "NonExistent")

        assert result == []

    def test_filter_with_all_values_set(self, nested_elements_with_parameters):
        """Test filtering elements where all parameter values are set"""
        result = getElementByParameterTypeWhereAllValuesAreSet(
            nested_elements_with_parameters, "Mass"
        )

        # Both elements with mass have values set (no "-")
        assert len(result) == 2

    def test_filter_with_unset_values(self):
        """Test filtering when some parameter values are not set"""
        mock_param_type = MagicMock()
        mock_param_type.Name = "Property"

        # Fully set parameter
        mock_param_set = MagicMock()
        mock_param_set.AssociatedParameter = MagicMock()
        mock_param_set.AssociatedParameter.ParameterType = mock_param_type
        mock_param_set.ActualValue = "value"

        # Unset parameter (represented as "-")
        mock_param_unset = MagicMock()
        mock_param_unset.AssociatedParameter = MagicMock()
        mock_param_unset.AssociatedParameter.ParameterType = mock_param_type
        mock_param_unset.ActualValue = "-"

        # Element with all values set
        mock_element_all_set = MagicMock()
        mock_element_all_set.NestedParameter = [mock_param_set]

        # Element with some unset values
        mock_element_some_unset = MagicMock()
        mock_element_some_unset.NestedParameter = [mock_param_set, mock_param_unset]

        elements = [mock_element_all_set, mock_element_some_unset]

        result = getElementByParameterTypeWhereAllValuesAreSet(elements, "Property")

        # Only first element should be returned (all values set)
        assert len(result) == 1
        assert mock_element_all_set in result

    def test_filter_with_multiple_unset_values(self):
        """Test filtering with multiple unset values"""
        mock_param_type = MagicMock()
        mock_param_type.Name = "Property"

        # Create parameters - some set, some unset
        params_unset = []
        for i in range(3):
            param = MagicMock()
            param.AssociatedParameter = MagicMock()
            param.AssociatedParameter.ParameterType = mock_param_type
            param.ActualValue = "-"
            params_unset.append(param)

        mock_element_unset = MagicMock()
        mock_element_unset.NestedParameter = params_unset

        result = getElementByParameterTypeWhereAllValuesAreSet([mock_element_unset], "Property")

        # Should be filtered out
        assert result == []


###################################################################################################
#                              TRANSACTION INTEGRATION TESTS                                     #
###################################################################################################


class TestTransactionIntegration:
    """Integration tests for transaction preparation and value setting"""

    def test_prepare_transaction_workflow(self, mock_iteration):
        """Test complete transaction preparation workflow"""
        with patch("comet_sdkp.CDP4Adaptor.ThingTransaction") as mock_tx_class:
            with patch("comet_sdkp.CDP4Adaptor.TransactionContextResolver") as mock_resolver:
                # Setup mocks
                mock_clone = MagicMock()
                mock_iteration.Clone.return_value = mock_clone

                mock_context = MagicMock()
                mock_resolver.ResolveContext.return_value = mock_context

                mock_transaction = MagicMock()
                mock_tx_class.return_value = mock_transaction

                # Prepare transaction
                cloned_iteration, transaction = prepareTransaction(mock_iteration)

                # Verify - prepareTransaction returns (clone, transaction)
                assert cloned_iteration == mock_clone  # Should be the clone, not original
                assert transaction == mock_transaction
                mock_iteration.Clone.assert_called_once_with(False)
                mock_resolver.ResolveContext.assert_called_once_with(mock_clone)

    def test_prepare_transaction_with_none(self):
        """Test preparing transaction with None iteration"""
        with pytest.raises(InvalidParametersException):
            prepareTransaction(None)

    def test_set_value_workflow_manual(self):
        """Test setting manual parameter values"""
        with patch("comet_sdkp.CDP4Adaptor.ParameterSwitchKind") as mock_switch_enum:
            with patch("comet_sdkp.CDP4Adaptor.Array"):
                with patch("comet_sdkp.CDP4Adaptor.ValueArray"):
                    mock_value_set = MagicMock()
                    mock_switch_kind = MagicMock()
                    mock_switch_kind.name = "MANUAL"
                    mock_switch_enum.MANUAL = mock_switch_kind

                    result = setValue(mock_value_set, mock_switch_kind, ["100", "200"])

                    assert result == mock_value_set
                    assert mock_value_set.ValueSwitch == mock_switch_kind

    def test_set_value_workflow_computed(self):
        """Test setting computed parameter values"""
        with patch("comet_sdkp.CDP4Adaptor.ParameterSwitchKind") as mock_switch_enum:
            with patch("comet_sdkp.CDP4Adaptor.Array"):
                with patch("comet_sdkp.CDP4Adaptor.ValueArray"):
                    mock_value_set = MagicMock()
                    mock_switch_kind = MagicMock()
                    mock_switch_kind.name = "COMPUTED"
                    mock_switch_enum.COMPUTED = mock_switch_kind

                    result = setValue(mock_value_set, mock_switch_kind, ["=Mass*Density"])

                    assert result == mock_value_set
                    assert mock_value_set.ValueSwitch == mock_switch_kind

    def test_set_value_workflow_reference(self):
        """Test setting reference parameter values"""
        with patch("comet_sdkp.CDP4Adaptor.ParameterSwitchKind") as mock_switch_enum:
            with patch("comet_sdkp.CDP4Adaptor.Array"):
                with patch("comet_sdkp.CDP4Adaptor.ValueArray"):
                    mock_value_set = MagicMock()
                    mock_switch_kind = MagicMock()
                    mock_switch_kind.name = "REFERENCE"
                    mock_switch_enum.REFERENCE = mock_switch_kind

                    result = setValue(mock_value_set, mock_switch_kind, ["ref-id"])

                    assert result == mock_value_set
                    assert mock_value_set.ValueSwitch == mock_switch_kind

    def test_set_value_with_none_value_set(self):
        """Test setting value with None value set"""
        with pytest.raises(InvalidParametersException):
            setValue(None, MagicMock(), ["100"])

    def test_set_value_with_none_values(self):
        """Test setting value with None values list"""
        with pytest.raises(InvalidParametersException):
            setValue(MagicMock(), MagicMock(), None)

    def test_set_value_with_empty_values(self):
        """Test setting value with empty values list"""
        with pytest.raises(InvalidParametersException):
            setValue(MagicMock(), MagicMock(), [])

    def test_set_value_with_invalid_switch_kind(self):
        """Test setting value with invalid switch kind"""
        mock_value_set = MagicMock()
        invalid_switch = MagicMock()
        invalid_switch.name = "INVALID"

        with patch("comet_sdkp.CDP4Adaptor.ParameterSwitchKind") as mock_switch_enum:
            with patch("comet_sdkp.CDP4Adaptor.Array"):
                with patch("comet_sdkp.CDP4Adaptor.ValueArray"):
                    mock_switch_enum.COMPUTED = MagicMock()
                    mock_switch_enum.MANUAL = MagicMock()
                    mock_switch_enum.REFERENCE = MagicMock()

                    with pytest.raises(ValueError) as exc_info:
                        setValue(mock_value_set, invalid_switch, ["100"])

                    assert "not recognized" in str(exc_info.value).lower()


###################################################################################################
#                            END-TO-END WORKFLOW INTEGRATION TESTS                               #
###################################################################################################


class TestEndToEndWorkflows:
    """Integration tests for complete end-to-end workflows"""

    def test_complete_product_tree_and_filtering_workflow(self, mock_iteration, mock_option):
        """Test workflow: compute tree -> filter by parameter -> get values"""
        with patch("comet_sdkp.CDP4Adaptor.NestedElementTreeGenerator") as mock_generator:
            # Create mock parameter
            mock_param_type = MagicMock()
            mock_param_type.Name = "Mass"

            mock_param = MagicMock()
            mock_param.AssociatedParameter = MagicMock()
            mock_param.AssociatedParameter.ParameterType = mock_param_type
            mock_param.ActualValue = "150"

            mock_nested_element = MagicMock()
            mock_nested_element.Name = "Component"
            mock_nested_element.NestedParameter = [mock_param]

            # Setup generator
            generator_instance = MagicMock()
            generator_instance.GenerateNestedElements.return_value = [mock_nested_element]
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

            # Verify the parameter value
            assert complete[0].NestedParameter[0].ActualValue == "150"

    def test_transaction_and_write_workflow(self, mock_session_service, mock_iteration):
        """Test workflow: prepare transaction -> set values -> write"""
        mock_session_service.isSessionOpen = True
        mock_session_service.session = MagicMock()

        mock_clone = MagicMock()
        mock_iteration.Clone.return_value = mock_clone

        with patch("comet_sdkp.CDP4Adaptor.ThingTransaction") as mock_tx_class:
            with patch("comet_sdkp.CDP4Adaptor.TransactionContextResolver") as mock_resolver:
                # Step 1: Prepare transaction
                mock_context = MagicMock()
                mock_resolver.ResolveContext.return_value = mock_context

                mock_transaction = MagicMock()
                mock_transaction.FinalizeTransaction.return_value = MagicMock()
                mock_tx_class.return_value = mock_transaction

                cloned_iteration, transaction = prepareTransaction(mock_iteration)
                # prepareTransaction returns (clone, transaction)
                assert cloned_iteration == mock_clone
                assert transaction is not None

                # Step 2: Write transaction
                mock_session_service.session.Write.return_value.GetAwaiter.return_value.GetResult.return_value = (
                    None
                )
                result = mock_session_service.write(transaction)

                # Verify write was called
                assert result is None
                mock_session_service.session.Write.assert_called_once()

    def test_complete_session_models_domains_workflow(
        self, mock_session_service, mock_person, mock_domain
    ):
        """Test complete workflow: session -> models -> domains -> details"""
        # Setup session
        mock_session_service.session = MagicMock()
        mock_session_service.isSessionOpen = True
        mock_session_service.session.ActivePerson = mock_person

        # Create models
        mock_participant = MagicMock()
        mock_participant.Person.Iid = "person-123"

        mock_model1 = MagicMock()
        mock_model1.Name = "Model A"
        mock_model1.Participant = [mock_participant]

        mock_model2 = MagicMock()
        mock_model2.Name = "Model B"
        mock_model2.Participant = [mock_participant]

        mock_site_dir = MagicMock()
        mock_site_dir.Model = [mock_model1, mock_model2]

        mock_session_service.session.RetrieveSiteDirectory.return_value = mock_site_dir

        # Step 1: Get models
        models = mock_session_service.getParticipantModels()
        assert len(models) == 2

        # Step 2: Get domains for first model
        mock_participant_with_domains = MagicMock()
        mock_participant_with_domains.Domain = [mock_domain]

        mock_model1.Participant = MagicMock()
        mock_model1.Participant.Find.return_value = mock_participant_with_domains

        domains = mock_session_service.getAvailableDomains(mock_model1)
        assert len(domains) == 1
        assert mock_domain in domains


###################################################################################################
#                        REAL INTEGRATION TESTS (Require CDP4 Server)                            #
###################################################################################################


@pytest.mark.integration
class TestRealCDP4Integration:
    """Integration tests against a real CDP4 server

    These tests require a running CDP4 server at http://localhost:5000
    with username 'admin' and password 'pass'

    To enable these tests, set the skipif parameter to False.
    """

    @pytest.mark.skipif(
        True,  # Set to False when CDP4 server is available
        reason="Requires CDP4 server at http://localhost:5000. Disable this skip condition to run.",
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
            assert hasattr(site_dir, "Model")
        finally:
            # Cleanup
            if service.isSessionOpen:
                service.close()

    @pytest.mark.skipif(
        True,
        reason="Requires CDP4 server at http://localhost:5000. Disable this skip condition to run.",
    )
    def test_real_get_participant_models(self):
        """Test getting participant models from real server"""
        service = Cdp4SessionService()

        result = service.open("http://localhost:5000", "admin", "pass")

        try:
            assert service.isSessionOpen is True

            models = service.getParticipantModels()
            assert isinstance(models, list)
            # Verify we got some models (may be 0 if test account has no models)
            assert len(models) >= 0
        finally:
            if service.isSessionOpen:
                service.close()

    @pytest.mark.skipif(
        True,
        reason="Requires CDP4 server at http://localhost:5000 with test data. Disable this skip condition to run.",
    )
    def test_real_open_iteration(self):
        """Test opening an actual iteration from real server"""
        service = Cdp4SessionService()

        result = service.open("http://localhost:5000", "admin", "pass")

        try:
            assert service.isSessionOpen is True

            models = service.getParticipantModels()
            assert isinstance(models, list)

            # If there are models, try to get their domains
            if len(models) > 0:
                model = models[0]
                site_dir = service.session.RetrieveSiteDirectory()

                # Find the corresponding setup
                setups = [m for m in site_dir.Model if m.Iid == model.Iid]

                if len(setups) > 0:
                    setup = setups[0]
                    domains = service.getAvailableDomains(setup)
                    assert isinstance(domains, list)
        finally:
            if service.isSessionOpen:
                service.close()
