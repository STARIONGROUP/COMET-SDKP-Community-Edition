"""

Module: CDP4Adaptor

Description:
    This module serves as a wrapper to the C++ CDP4 SDK in python.

Scope:
    This module is part of the integration between COMET and YODA.

Author:
    STARION GROUP

Created:
    2026-01-09

Version:
    0.1.0

License:
    LGPL-2.1 license

Dependencies:
    - pythonnet

Notes:
    This module is a first approach to covering all the CDP4 functionalities with a python library.

"""

###################################################################################################
#                                                                                                 #
#                                            IMPORTS                                              #
#                                                                                                 #
###################################################################################################

import sys
import os
from typing import List, Tuple, Optional, Union, Any
from pathlib import Path
import logging

import clr

# Configure logging
logger = logging.getLogger(__name__)

# Load native libraries
_SCRIPT_DIR = Path(__file__).parent
_DLL_FOLDER = _SCRIPT_DIR / "libs"
sys.path.insert(0, str(_DLL_FOLDER))

try:
    clr.AddReference("CDP4ServicesDal")
except Exception as e:
    logger.critical(f"Error loading DLL: {e}")
    raise ImportError(f"Failed to load CDP4ServicesDal: {e}") from e

from System import Guid, Uri, Predicate, String, Array
from System.Threading import CancellationTokenSource

from CDP4Common.Helpers import NestedElementTreeGenerator
from CDP4Common.EngineeringModelData import (
    Iteration,
    EngineeringModel,
    Option,
    NestedElement,
    NestedParameter,
    ParameterValueSetBase,
    ParameterSwitchKind,
)
from CDP4Common.SiteDirectoryData import (
    EngineeringModelSetup,
    SiteDirectory,
    DomainOfExpertise,
    Participant,
)
from CDP4Common.Types import ValueArray
from CDP4Dal import Session, CDPMessageBus
from CDP4Dal.DAL import Credentials
from CDP4Dal.Operations import OperationContainer, ThingTransaction, TransactionContextResolver
from CDP4ServicesDal import CdpServicesDal

###################################################################################################
#                                                                                                 #
#                                        EXCEPTIONS                                               #
#                                                                                                 #
###################################################################################################


class Cdp4Exception(Exception):
    """Base exception for CDP4 operations"""

    pass


class SessionException(Cdp4Exception):
    """Exception raised when session operations fail"""

    pass


class InvalidParametersException(Cdp4Exception):
    """Exception raised when invalid parameters are provided"""

    pass


###################################################################################################
#                                                                                                 #
#                                            CLASSES                                              #
#                                                                                                 #
###################################################################################################


class Cdp4SessionService:
    """
    Python wrapper around the CDP4 Session to allow communication with the CDP4-COMET server.

    This class manages the lifecycle of a CDP4 session and provides high-level methods
    for interacting with CDP4 servers.

    Attributes:
        session (Session | None): The underlying CDP4 session object
        dal (CdpServicesDal): Data access layer
        messageBus (CDPMessageBus): Message communication bus
        isSessionOpen (bool): Current session connection status
    """

    # Class-level constants
    _ACTIVE_ITERATION_MARKER = None  # FrozenOn == None indicates active iteration

    def __init__(self):
        """
        Initializes a new instance of the Cdp4SessionService class.

        Raises:
            Cdp4Exception: If initialization of core components fails
        """
        super().__init__()

        try:
            self.session: Optional[Session] = None
            self.dal = CdpServicesDal(None)
            self.messageBus = CDPMessageBus()
            self.isSessionOpen = False
        except Exception as e:
            logger.error(f"Failed to initialize Cdp4SessionService: {e}")
            raise Cdp4Exception(f"Service initialization failed: {e}") from e

    def open(
        self, serverUri: str, userName: str, password: str, timeout_seconds: int = 30
    ) -> Optional[str]:
        """
        Opens a session to the CDP4-COMET server.

        Args:
            serverUri: The URI to reach the CDP4-COMET server (e.g., http://localhost:5000)
            userName: The username to use for authentication
            password: The password to use for authentication
            timeout_seconds: Connection timeout in seconds (default: 30)

        Returns:
            None if the session opened successfully, error string otherwise

        Raises:
            SessionException: If session is already open
            InvalidParametersException: If required parameters are missing or invalid
        """
        # Validate input parameters
        self._validate_string_parameter(serverUri, "Server URI")
        self._validate_string_parameter(userName, "Username")
        self._validate_string_parameter(password, "Password")

        if self.isSessionOpen:
            error_msg = "Session already open. Close the existing session before opening a new one."
            logger.warning(error_msg)
            raise SessionException(error_msg)

        try:
            uri = Uri(serverUri)
            credentials = Credentials(userName, password, uri)
            self.session = Session(self.dal, credentials, self.messageBus)

            logger.info(f"Opening session to {serverUri}...")
            self.session.Open().GetAwaiter().GetResult()

            self.isSessionOpen = True
            logger.info(f"Session initialized against {serverUri}: Success")
            return None

        except Exception as e:
            logger.error(f"Error during session opening: {e}")
            self.isSessionOpen = False
            self.session = None
            return str(e)

    def close(self) -> Optional[str]:
        """
        Closes the current session.

        Returns:
            None if the session closed successfully, error string otherwise
        """
        if not self.isSessionOpen or self.session is None:
            logger.warning("No active session to close")
            return None

        try:
            self.session.Close().GetAwaiter().GetResult()
            self.isSessionOpen = False
            self.session = None
            logger.info("Session closed successfully")
            return None
        except Exception as e:
            logger.error(f"Error during session closing: {e}")
            return str(e)

    def getParticipantModels(self) -> List[EngineeringModelSetup]:
        """
        Gets the collection of EngineeringModelSetup that the current user is participating in.

        Returns:
            List of available EngineeringModelSetup. Returns empty list if session is not open.

        Raises:
            SessionException: If session is not open
        """
        if not self.isSessionOpen:
            logger.warning("Cannot get participant models: session is not open")
            return []

        if self.session is None:
            logger.error("Session object is None despite isSessionOpen being True")
            return []

        try:
            site_directory = self.session.RetrieveSiteDirectory()
            if not site_directory or not site_directory.Model:
                logger.debug("No models found in site directory")
                return []

            target_iid = self.session.ActivePerson.Iid

            # Filter models where current user is a participant
            filtered_models = [
                model
                for model in site_directory.Model
                if any(participant.Person.Iid == target_iid for participant in model.Participant)
            ]

            logger.info(f"Found {len(filtered_models)} participant models")
            return filtered_models

        except Exception as e:
            logger.error(f"Error retrieving participant models: {e}")
            return []

    def getAvailableDomains(
        self, engineeringModelSetup: EngineeringModelSetup
    ) -> List[DomainOfExpertise]:
        """
        Gets the collection of DomainOfExpertise that the current user can access for a specific model.

        Args:
            engineeringModelSetup: The EngineeringModelSetup to get domains for

        Returns:
            List of available DomainOfExpertise for the user in this model

        Raises:
            SessionException: If session is not open
            InvalidParametersException: If engineeringModelSetup is None
        """
        if not self.isSessionOpen:
            logger.warning("Cannot get available domains: session is not open")
            return []

        if engineeringModelSetup is None:
            error_msg = "engineeringModelSetup parameter cannot be None"
            logger.error(error_msg)
            raise InvalidParametersException(error_msg)

        try:
            predicate = Predicate[Participant](
                lambda x: x.Person.Iid == self.session.ActivePerson.Iid
            )
            participant = engineeringModelSetup.Participant.Find(predicate)

            if not participant:
                logger.debug(f"User is not a participant in model {engineeringModelSetup.Name}")
                return []

            domains = list(participant.Domain) if participant.Domain else []
            logger.info(
                f"Found {len(domains)} available domains for model {engineeringModelSetup.Name}"
            )
            return domains

        except Exception as e:
            logger.error(f"Error retrieving available domains: {e}")
            return []

    def openActiveIteration(
        self,
        engineeringModelSetup: EngineeringModelSetup,
        selectedDomainOfExpertise: DomainOfExpertise,
    ) -> Union[Any, str]:
        """
        Opens the active Iteration of the provided EngineeringModelSetup for the selected domain.

        Args:
            engineeringModelSetup: The EngineeringModelSetup to open
            selectedDomainOfExpertise: The DomainOfExpertise to use

        Returns:
            The opened Iteration on success, error string on failure

        Raises:
            InvalidParametersException: If required parameters are None
            SessionException: If session is not open
        """
        if engineeringModelSetup is None:
            error_msg = "engineeringModelSetup parameter cannot be None"
            logger.error(error_msg)
            raise InvalidParametersException(error_msg)

        if selectedDomainOfExpertise is None:
            error_msg = "selectedDomainOfExpertise parameter cannot be None"
            logger.error(error_msg)
            raise InvalidParametersException(error_msg)

        if not self.isSessionOpen:
            error_msg = "Session is not open"
            logger.error(error_msg)
            return error_msg

        try:
            # Find the active iteration (FrozenOn == None)
            active_iteration_setup = self._get_active_iteration_setup(engineeringModelSetup)
            
            if active_iteration_setup is None:
                error_msg = f"No active iteration found for model {engineeringModelSetup.Name}"
                logger.warning(error_msg)
                return error_msg

            # Create and read the iteration
            engineering_model = EngineeringModel()
            engineering_model.Iid = engineeringModelSetup.EngineeringModelIid
            
            iteration = Iteration()
            iteration.Iid = getattr(active_iteration_setup, 'IterationIid', None)
            engineering_model.Iteration.Add(iteration)

            logger.info(f"Reading iteration {iteration.Iid} for domain {selectedDomainOfExpertise.Name}...")
            self.session.Read(iteration, selectedDomainOfExpertise).GetAwaiter().GetResult()

            # Retrieve the opened iteration from session
            iteration_iid = getattr(active_iteration_setup, 'IterationIid', None)
            opened_iteration = self._get_opened_iteration(iteration_iid)
            
            if isinstance(opened_iteration, str):
                error_msg = "Failed to open iteration - returned error string"
                logger.error(error_msg)
                return error_msg

            if opened_iteration is None:
                error_msg = "Failed to open iteration - not found in session"
                logger.error(error_msg)
                return error_msg

            logger.info(f"Successfully opened iteration {opened_iteration.Iid}")
            return opened_iteration
            
        except Exception as e:
            logger.error(f"Error opening active iteration: {e}")
            return str(e)

    def write(self, thingTransaction: ThingTransaction) -> Optional[str]:
        """
        Writes an OperationContainer to the Session.

        Args:
            thingTransaction: The ThingTransaction containing changes

        Returns:
            None if successful, error string otherwise

        Raises:
            SessionException: If session is not open
            InvalidParametersException: If thingTransaction is None
        """
        if not self.isSessionOpen:
            error_msg = "Session is not open"
            logger.error(error_msg)
            raise SessionException(error_msg)

        if thingTransaction is None:
            error_msg = "thingTransaction parameter cannot be None"
            logger.error(error_msg)
            raise InvalidParametersException(error_msg)

        try:
            logger.info("Writing transaction to server...")
            self.session.Write(thingTransaction.FinalizeTransaction()).GetAwaiter().GetResult()
            logger.info("Transaction written successfully")
            return None

        except Exception as e:
            logger.error(f"Error during write operation: {e}")
            return str(e)

    # ======================== Private Helper Methods ========================

    @staticmethod
    def _validate_string_parameter(value: str, param_name: str) -> None:
        """
        Validates that a string parameter is not None or empty.

        Args:
            value: The value to validate
            param_name: The parameter name for error messages

        Raises:
            InvalidParametersException: If value is None or empty
        """
        if not value or not isinstance(value, str):
            error_msg = f"{param_name} must be a non-empty string"
            logger.error(error_msg)
            raise InvalidParametersException(error_msg)

    def _get_active_iteration_setup(
        self, 
        model_setup: EngineeringModelSetup
    ) -> Optional[Any]:
        """
        Finds the active iteration setup for a model.

        Args:
            model_setup: The model setup to search

        Returns:
            The active iteration setup or None if not found
        """
        try:
            for iteration_setup in model_setup.IterationSetup:
                if iteration_setup.FrozenOn is None:  # Active iteration not frozen
                    return iteration_setup
            return None
        except Exception as e:
            logger.error(f"Error getting active iteration setup: {e}")
            return None

    def _get_opened_iteration(self, iteration_iid: Any) -> Optional[Any]:
        """
        Retrieves an opened iteration from the session.

        Args:
            iteration_iid: The iteration IID to find

        Returns:
            The Iteration object or None if not found
        """
        if self.session is None:
            return None
        
        try:
            opened_iterations_keys = self.session.OpenIterations.Keys
            return next(
                (x for x in opened_iterations_keys if x.Iid == iteration_iid),
                None
            )
        except Exception as e:
            logger.error(f"Error getting opened iteration: {e}")
            return None


###################################################################################################
#                                                                                                 #
#                                           FUNCTIONS                                             #
#                                                                                                 #
###################################################################################################


def computeProductTree(iteration: Iteration, option: Option) -> List[NestedElement]:
    """
    Computes a Product Tree based on the TopElement of the provided Iteration for the specified option.

    Args:
        iteration: The iteration to use to generate the Product Tree
        option: The selected Option

    Returns:
        List of NestedElement objects that compose the Product Tree.
        Returns empty list if tree generation fails.

    Raises:
        InvalidParametersException: If required parameters are None
    """
    if iteration is None:
        error_msg = "iteration parameter cannot be None"
        logger.error(error_msg)
        raise InvalidParametersException(error_msg)

    if option is None:
        error_msg = "option parameter cannot be None"
        logger.error(error_msg)
        raise InvalidParametersException(error_msg)

    if iteration.TopElement is None:
        logger.warning("The iteration does not define a top element")
        return []

    try:
        logger.info(f"Generating product tree for option {option.Name}...")
        product_tree_generator = NestedElementTreeGenerator()

        # GenerateNestedElements returns IEnumerable[NestedElement] from .NET
        tree_enumerable = product_tree_generator.GenerateNestedElements(
            option, iteration.TopElement
        )

        # Convert IEnumerable[NestedElement] to Python list
        # Handle None case and conversion errors gracefully
        if tree_enumerable is None:
            logger.warning("GenerateNestedElements returned None")
            return []

        # Convert to list - try direct conversion first
        tree = []
        try:
            tree = list(tree_enumerable)
        except TypeError as type_error:
            # If direct conversion fails, iterate manually
            logger.debug(f"Direct list conversion failed: {type_error}, using manual iteration")
            for element in tree_enumerable:
                tree.append(element)

        logger.info(f"Generated product tree with {len(tree)} root elements")
        return tree

    except Exception as e:
        logger.error(f"Error computing product tree: {e}")
        # Return empty list instead of raising to maintain consistency with other functions
        return []


def getElementByParameterType(
    nestedElements: List[NestedElement], parameterTypeName: str
) -> List[NestedElement]:
    """
    Filters NestedElements to keep only those containing a Parameter with the specified ParameterType name.

    Args:
        nestedElements: The collection of NestedElement to filter
        parameterTypeName: The name of the ParameterType to filter by

    Returns:
        Filtered list of NestedElement objects

    Raises:
        InvalidParametersException: If required parameters are invalid
    """
    if not nestedElements:
        error_msg = "nestedElements list cannot be None or empty"
        logger.error(error_msg)
        raise InvalidParametersException(error_msg)

    if not parameterTypeName or not isinstance(parameterTypeName, str):
        error_msg = "parameterTypeName must be a non-empty string"
        logger.error(error_msg)
        raise InvalidParametersException(error_msg)

    try:
        matching_elements = [
            element
            for element in nestedElements
            if any(
                param.AssociatedParameter.ParameterType.Name == parameterTypeName
                for param in element.NestedParameter
            )
        ]

        logger.info(
            f"Found {len(matching_elements)} elements with parameter type '{parameterTypeName}'"
        )
        return matching_elements

    except Exception as e:
        logger.error(f"Error filtering elements by parameter type: {e}")
        return []


def getElementByParameterTypeWhereAllValuesAreSet(
    nestedElements: List[NestedElement], parameterTypeName: str
) -> List[NestedElement]:
    """
    Filters NestedElements to keep only those where all values for the parameter type are set.

    This function first filters by parameter type, then excludes elements where any value is unset ("-").

    Args:
        nestedElements: The collection of NestedElement to filter
        parameterTypeName: The name of the ParameterType to filter by

    Returns:
        Filtered list of NestedElement objects with all values set

    Raises:
        InvalidParametersException: If required parameters are invalid
    """
    try:
        # First filter by parameter type
        filtered_elements = getElementByParameterType(nestedElements, parameterTypeName)

        if not filtered_elements:
            logger.info(f"No elements found with parameter type '{parameterTypeName}'")
            return []

        # Then filter by complete values (no "-" unset values)
        elements_with_all_values = [
            element
            for element in filtered_elements
            if _has_all_values_set(element, parameterTypeName)
        ]

        logger.info(
            f"Found {len(elements_with_all_values)} elements with all values set "
            f"for parameter type '{parameterTypeName}'"
        )
        return elements_with_all_values

    except InvalidParametersException:
        raise
    except Exception as e:
        logger.error(f"Error filtering elements by complete parameter values: {e}")
        return []


def prepareTransaction(iteration: Iteration) -> Tuple[Iteration, ThingTransaction]:
    """
    Prepares a ThingTransaction based on an Iteration context.

    This creates a clone of the iteration and associates it with a transaction for modifications.

    Args:
        iteration: The Iteration to prepare for transactions

    Returns:
        Tuple of (cloned Iteration, associated ThingTransaction)

    Raises:
        InvalidParametersException: If iteration is None
    """
    if iteration is None:
        error_msg = "iteration parameter cannot be None"
        logger.error(error_msg)
        raise InvalidParametersException(error_msg)

    try:
        logger.info("Preparing transaction for iteration...")
        clone = iteration.Clone(False)
        transaction = ThingTransaction(TransactionContextResolver.ResolveContext(clone), clone)
        logger.info("Transaction prepared successfully")
        return clone, transaction

    except Exception as e:
        logger.error(f"Error preparing transaction: {e}")
        raise


def setValue(
    valueSet: ParameterValueSetBase, switchKind: ParameterSwitchKind, newValues: List[str]
) -> ParameterValueSetBase:
    """
    Sets the value of a ParameterValueSetBase for the specified ParameterSwitchKind.

    Args:
        valueSet: The ParameterValueSetBase to modify
        switchKind: The ParameterSwitchKind (MANUAL, COMPUTED, or REFERENCE)
        newValues: List of new values to set

    Returns:
        The updated ParameterValueSetBase

    Raises:
        InvalidParametersException: If parameters are invalid
        ValueError: If switchKind is not recognized
    """
    if valueSet is None:
        error_msg = "valueSet parameter cannot be None"
        logger.error(error_msg)
        raise InvalidParametersException(error_msg)

    if not newValues or not isinstance(newValues, list):
        error_msg = "newValues must be a non-empty list"
        logger.error(error_msg)
        raise InvalidParametersException(error_msg)

    try:
        # Convert list to ValueArray
        collection = Array[String](newValues)
        value_array = ValueArray[String](collection)

        logger.debug(
            f"Setting values with switch kind: {switchKind} (type: {type(switchKind).__name__})"
        )

        # Get the enum value name using multiple methods for compatibility
        switch_kind_name = None

        # Try to get the name attribute (works with some .NET enums)
        if hasattr(switchKind, "name"):
            switch_kind_name = switchKind.name.upper()
        # Try to convert to string and extract name (CDP4 convention: "MANUAL", "COMPUTED", "REFERENCE")
        elif hasattr(switchKind, "ToString"):
            switch_kind_str = switchKind.ToString()
            switch_kind_name = (
                switch_kind_str.split(".")[-1].upper()
                if "." in switch_kind_str
                else switch_kind_str.upper()
            )
        # Try to use string representation
        else:
            switch_kind_name = str(switchKind).upper()

        logger.debug(f"Switch kind name resolved to: {switch_kind_name}")

        # Set the appropriate value based on switch kind
        if "MANUAL" in switch_kind_name:
            valueSet.Manual = value_array
            logger.debug(f"Set MANUAL values: {newValues}")
        elif "COMPUTED" in switch_kind_name:
            valueSet.Computed = value_array
            logger.debug(f"Set COMPUTED values: {newValues}")
        elif "REFERENCE" in switch_kind_name:
            valueSet.Reference = value_array
            logger.debug(f"Set REFERENCE values: {newValues}")
        else:
            error_msg = f"ParameterSwitchKind '{switch_kind_name}' not recognized. Expected MANUAL, COMPUTED, or REFERENCE"
            logger.error(error_msg)
            raise ValueError(error_msg)

        valueSet.ValueSwitch = switchKind
        return valueSet

    except (InvalidParametersException, ValueError):
        raise
    except Exception as e:
        logger.error(f"Error setting value: {e}")
        raise InvalidParametersException(f"Error setting value: {e}") from e


# ======================== Private Helper Functions ========================


def _has_all_values_set(element: NestedElement, parameterTypeName: str) -> bool:
    """
    Checks if all values for a specific parameter type in an element are set.

    Args:
        element: The NestedElement to check
        parameterTypeName: The parameter type name to check

    Returns:
        True if all values are set (not "-"), False otherwise
    """
    matching_parameters = [
        param
        for param in element.NestedParameter
        if param.AssociatedParameter.ParameterType.Name == parameterTypeName
    ]

    return all(param.ActualValue != "-" for param in matching_parameters)
