import sys
import os
from typing import List, Tuple

import clr

script_dir = os.path.dirname(os.path.abspath(__file__))
dll_folder = os.path.join(script_dir, "DLLs")
sys.path.append(dll_folder)

try:
    clr.AddReference("CDP4ServicesDal")

except Exception as e:
    print(f"Error loading DLL: {e}")
    sys.exit(1)

from System import Guid, Uri, Predicate, String, Array
from System.Threading import CancellationTokenSource

from CDP4Common.Helpers import NestedElementTreeGenerator
from CDP4Common.EngineeringModelData import Iteration, EngineeringModel, Option, NestedElement, NestedParameter, ParameterValueSetBase, ParameterSwitchKind
from CDP4Common.SiteDirectoryData import EngineeringModelSetup, SiteDirectory, DomainOfExpertise, Participant
from CDP4Common.Types import ValueArray
from CDP4Dal import Session, CDPMessageBus
from CDP4Dal.DAL import Credentials
from CDP4Dal.Operations import OperationContainer, ThingTransaction, TransactionContextResolver
from CDP4ServicesDal import CdpServicesDal

class Cdp4SessionService:
    """Python around the Session to allow communication with the CDP4-COMET server"""
    def __init__(self):
        """
        Initializes a new instance of the Cdp4Session class
        """
        super().__init__()

        self.session = None
        self.dal = CdpServicesDal(None)
        self.messageBus = CDPMessageBus()
        self.isSessionOpen = False

    def open(self, serverUri: str, userName: str, password: str) -> None | str:
        """
        Opens a session to the CDP4-COMET server

        :param serverUri: The URI to reach the CDP4-COMET server
        :param userName: The username to use for authentication
        :param password: The password to use for authentication
        :return: None if the session could be open with success, the error otherwise
        """
        if self.isSessionOpen:
            return "Session already open"

        if not serverUri:
            return "Server URI not provided"

        if not userName:
            return "Username not provided"

        if not password:
            return "Password not provided"

        uri = Uri(serverUri)
        credentials = Credentials(userName, password, uri)
        try:
            self.session = Session(self.dal, credentials, self.messageBus)
            self.session.Open().GetAwaiter().GetResult()
            print(f"Session initialized against {serverUri}: Success")
            self.isSessionOpen = True
        except Exception as e:
            print(f"Error during session opening: {e}")
            return str(e)

    def getParticipantModels(self) -> List[EngineeringModelSetup]:
        """
        Gets the collection of EngineeringModelSetup that the current user is participating on
        :return: The collection of available EngineeringModelSetup. If the session is not open, the list is empty
        """
        if not self.isSessionOpen:
            return []

        models = self.session.RetrieveSiteDirectory().Model
        target_iid = self.session.ActivePerson.Iid

        filtered_result = [
            x for x in models
            if any(p.Person.Iid == target_iid for p in x.Participant)
        ]

        return filtered_result

    def getAvailableDomains(self, engineeringModelSetup: EngineeringModelSetup) -> List[DomainOfExpertise]:
        """
        Gets the collection of DomainOfExpertise that the current user can access for a specific EngineeringModelSetup
        :param engineeringModelSetup: The EngineeringModelSetup that the current user is participating on
        :return: A collection of available DomainOfExpertise.
        """
        if not self.isSessionOpen:
            return []

        if not engineeringModelSetup:
            raise ValueError("The EngineeringModelSetup must be provided")

        predicate = Predicate[Participant](lambda x: x.Person.Iid == self.session.ActivePerson.Iid)
        participant = engineeringModelSetup.Participant.Find(predicate)

        if not participant:
            return []

        return participant.Domain

    def openActiveIteration(self, engineeringModelSetup: EngineeringModelSetup, selectedDomainOfExpertise: DomainOfExpertise) -> Iteration | str:
        """
        Opens the active Iteration of the provided EngineeringModelSetup for the selected DomainOfExpertise
        :param engineeringModelSetup: The selected EngineeringModelSetup to open
        :param selectedDomainOfExpertise: The selected DomainOfExpertise to use
        :return: The opened Iteration in case of success, the error string otherwise
        """
        if not engineeringModelSetup:
            raise ValueError("The EngineeringModelSetup must be provided")

        if not selectedDomainOfExpertise:
            raise ValueError("The DomainOfExpertise must be provided")

        if not self.isSessionOpen:
            return "Session is not open"

        activeIterationSetup = None

        for iterationSetup in engineeringModelSetup.IterationSetup:
            if iterationSetup.FrozenOn == None:
                activeIterationSetup = iterationSetup
                break

        engineeringModel = EngineeringModel()
        engineeringModel.Iid = engineeringModelSetup.EngineeringModelIid
        iteration = Iteration()
        iteration.Iid = activeIterationSetup.IterationIid

        engineeringModel.Iteration.Add(iteration)

        self.session.Read(iteration, selectedDomainOfExpertise).GetAwaiter().GetResult()

        openedIterationsKeys = self.session.OpenIterations.Keys
        openedIteration = next((x for x in openedIterationsKeys if x.Iid == activeIterationSetup.IterationIid), None)

        if isinstance(openedIteration, Iteration):
            return openedIteration

        return "Failed to open Iteration"

    def write(self, thingTransaction: ThingTransaction) -> None | str:
        """
        Writes an OperationContainer to the Session
        :param thingTransaction: The OperationContainer
        :return: None if the operation went successfully, the exception string otherwise
        """
        if not self.isSessionOpen:
            return "Session is not open"

        if not thingTransaction:
            return "ThingTransaction must be provided"

        try:
            self.session.Write(thingTransaction.FinalizeTransaction()).GetAwaiter().GetResult()
        except Exception as e:
            print(f"Error during write operation: {e}")
            return str(e)


def computeProductTree(iteration: Iteration, option: Option) -> List[NestedElement]:
    """
    Computes a Product Tree based on the TopElement of the provided Iteration, for the specified option
    :param iteration: The iteration to use to generate the Product Tree
    :param option: The selected Option
    :return: A collection of NestedElement that composes the Product Tree
    """
    if not option:
        raise ValueError("The Option must be provided")

    if not iteration:
        raise ValueError("The Iteration must be provided")

    if not iteration.TopElement:
        print("The iteration does not define a top element")
        return []

    productTreeGenerator = NestedElementTreeGenerator()
    return productTreeGenerator.GenerateNestedElements(option, iteration.TopElement)

def getElementByParameterType(nestedElements: List[NestedElement], parameterTypeName: str) -> List[NestedElement]:
    """
    Filter the collection of NestedElement to only keep Element that contains a Parameter where the ParameterType Name
    matches the provides name
    :param nestedElements: The collection of NestedElement that should be filtered
    :param parameterTypeName: The name of the ParameterType to filter by
    :return: A filtered collection
    """
    if not nestedElements:
        raise ValueError("The nestedElements must be provided")

    if not parameterTypeName:
        raise ValueError("The parameter type Name must be provided")

    matchingNestedElements = []

    for nestedElement in nestedElements:
        if any(p.AssociatedParameter.ParameterType.Name == parameterTypeName for p in nestedElement.NestedParameter):
            matchingNestedElements.append(nestedElement)

    return matchingNestedElements

def getElementByParameterTypeWhereAllValuesAreSet(nestedElements: List[NestedElement], parameterTypeName: str) -> List[NestedElement]:
    """
    Filter the collection of NestedElement to only keep Element that contains a Parameter where the ParameterType Name
    matches the provides name and if all ActualValue are set
    :param nestedElements: The collection of NestedElement that should be filtered
    :param parameterTypeName: The name of the ParameterType to filter by
    :return: A filtered collection
    """
    filteredElements = getElementByParameterType(nestedElements, parameterTypeName)

    elemetsWithAllValues = []

    for nestedElement in filteredElements:
        matchingParameters = [p for p in nestedElement.NestedParameter if p.AssociatedParameter.ParameterType.Name == parameterTypeName]
        allDifferent = all(x.ActualValue != "-" for x in matchingParameters)

        if allDifferent:
            elemetsWithAllValues.append(nestedElement)

    return elemetsWithAllValues

def prepareTransaction(iteration: Iteration) -> Tuple[Iteration, ThingTransaction]:
    """
    Prepares a ThingTransaction based on an Iteration context
    :param iteration: The Iteration
    :return: The cloned Iteration and the associated ThingTransaction,
    """
    if not iteration:
        raise ValueError("The Iteration must be provided")

    clone = iteration.Clone(False)
    transaction = ThingTransaction(TransactionContextResolver.ResolveContext(clone), clone)
    return iteration, transaction

def setValue(valueSet: ParameterValueSetBase, switchKind: ParameterSwitchKind, newValues: List[str]) -> ParameterValueSetBase:
    """
    Sets the value of a ParameterValueSetBase for the specified ParameterSwitchKind
    :param valueSet: The ParameterValueSetBase
    :param switchKind: The targeted ParameterSwitchKind to update
    :param newValues: The list of new values to set
    :return: The updated ParameterValueSetBase
    """
    collection = Array[String](newValues)
    valueArray = ValueArray[String](collection)

    if switchKind == ParameterSwitchKind.COMPUTED:
        valueSet.Computed = valueArray
    elif switchKind == ParameterSwitchKind.MANUAL:
        valueSet.Manual = valueArray
    elif switchKind == ParameterSwitchKind.REFERENCE:
        valueSet.Reference = valueArray
    else:
        raise ValueError(f"ParameterSwitchKind {switchKind} not recognized")

    valueSet.ValueSwitch = switchKind
    return valueSet