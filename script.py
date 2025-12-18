from CDP4Adaptor import *

def main():
    session = Cdp4SessionService()
    openResult = session.open("http://localhost:5000", "admin", "pass")

    if openResult:
        print(f"Failed to open session: {openResult}")
        return

    participantModels = session.getParticipantModels()

    for model in participantModels:
        print(f'Participant into: {model.Name}')

        domains = session.getAvailableDomains(model)

        for domain in domains:
            print(f'Available domain: {domain.Name} ({domain.ShortName})')

        iteration = session.openActiveIteration(model, domains[0])

        if isinstance(iteration, str):
            print(iteration)
            return
        else:
            print("Iteration opened successfully")

        parameterTypeName = "electric current"

        for option in iteration.Option:
            print(f"Generating ProductTree for option: {option.Name}")

            productTree = computeProductTree(iteration, option)
            filteredByElectricCurrent = getElementByParameterTypeWhereAllValuesAreSet(productTree, parameterTypeName)

            sumValue = 0

            for element in sorted(filteredByElectricCurrent, key=lambda x: x.ShortName.count(".")):
                matchingParameters = [p for p in element.NestedParameter if p.AssociatedParameter.ParameterType.Name == parameterTypeName]
                for parameter in matchingParameters:
                    sumValue += int(parameter.ActualValue)

            print(f"Sum Value: {sumValue}")

            clonedIteration, transaction = prepareTransaction(iteration)
            parameter = clonedIteration.TopElement.Parameter[0].Clone(True)
            transaction.CreateOrUpdate(parameter)

            stateIndex = 1

            for valueSet in parameter.ValueSet:
                transaction.CreateOrUpdate(setValue(valueSet, ParameterSwitchKind.COMPUTED, [str(sumValue/stateIndex)]))
                stateIndex += 1
            writeResult = session.write(transaction)

            if isinstance(writeResult, str):
                print(writeResult)
            else:
                print("Write operation successful")

if __name__ == "__main__":
    main()