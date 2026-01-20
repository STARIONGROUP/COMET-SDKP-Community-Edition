"""
Basic connection example for CDP4 Python Adaptor

WARNING:
    This script connects to a real backend and may modify data.
    Do not run in production environments.

Requirements:
    - Running CDP4-COMET server at http://localhost:5000
    - Valid credentials (default: admin/pass)
    - At least one model where the user is a participant
    - At least one option in the active iteration

Usage:
    python script.py

"""

import logging
from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    getElementByParameterType,
    getElementByParameterTypeWhereAllValuesAreSet,
    prepareTransaction,
    setValue,
    SessionException,
    InvalidParametersException,
)
from CDP4Common.EngineeringModelData import ParameterSwitchKind

# Configure logging to see debug messages
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Get logger instance for this module
logger = logging.getLogger(__name__)


def main():
    """
    Main function demonstrating a complete CDP4 workflow.

    Workflow:
    1. Open session to CDP4 server
    2. Retrieve participant models
    3. For each model:
       - Get available domains
       - Open active iteration
       - Compute product tree for each option
       - Filter elements by parameter type
       - Calculate sum of parameter values
       - Create transaction and update parameters
       - Write changes back to server

    Raises:
        SessionException: If session operations fail
        InvalidParametersException: If invalid parameters are provided
    """
    session = Cdp4SessionService()

    # Step 1: Open session
    print("Opening session to CDP4 server...")
    open_result = session.open("http://localhost:5000", "admin", "pass")

    if open_result is not None:  # open() returns None on success, error string on failure
        print(f"❌ Failed to open session: {open_result}")
        return

    print("✅ Session opened successfully")

    # Step 2: Get participant models
    print("\nRetrieving participant models...")
    participant_models = session.getParticipantModels()

    if not participant_models:
        print("❌ No participant models found")
        session.close()
        return

    print(f"✅ Found {len(participant_models)} participant model(s)")

    # Step 3: Process each model
    for model in participant_models:
        print(f"\n{'='*60}")
        print(f"Processing model: {model.Name}")
        print(f"{'='*60}")

        # Get available domains for this model
        try:
            domains = session.getAvailableDomains(model)
        except InvalidParametersException as e:
            print(f"❌ Error getting domains: {e}")
            continue

        if not domains:
            print("⚠️  No available domains for this model")
            continue

        print(f"✅ Found {len(domains)} domain(s)")

        # Display available domains
        for domain in domains:
            domain_display = f"{domain.Name}"
            if hasattr(domain, "ShortName") and domain.ShortName:
                domain_display += f" ({domain.ShortName})"
            print(f"   - {domain_display}")

        # Open active iteration
        print(f"\nOpening active iteration...")
        try:
            iteration = session.openActiveIteration(model, domains[0])
        except InvalidParametersException as e:
            print(f"❌ Error opening iteration: {e}")
            continue

        # Check if iteration was successfully opened
        if isinstance(iteration, str):
            print(f"❌ Failed to open iteration: {iteration}")
            continue

        print("✅ Iteration opened successfully")

        # Step 4: Process options in iteration
        if not hasattr(iteration, "Option") or not iteration.Option:
            print("⚠️  No options available in this iteration")
            continue

        parameter_type_name = "electric current"

        for option in iteration.Option:
            print(f"\n{'─'*60}")
            print(f"Processing option: {option.Name}")
            print(f"{'─'*60}")

            # Generate product tree for this option
            print(f"Generating ProductTree for option: {option.Name}")
            try:
                product_tree = computeProductTree(iteration, option)
            except InvalidParametersException as e:
                print(f"❌ Error computing product tree: {e}")
                continue
            except Exception as e:
                print(f"❌ Unexpected error computing product tree: {e}")
                continue

            if not product_tree:
                print(f"⚠️  Product tree is empty for option {option.Name}")
                continue

            print(f"✅ Generated product tree with {len(product_tree)} element(s)")

            # Filter elements by parameter type (with all values set)
            print(f"Filtering elements with '{parameter_type_name}' parameter...")
            try:
                filtered_elements = getElementByParameterTypeWhereAllValuesAreSet(
                    product_tree, parameter_type_name
                )
            except InvalidParametersException as e:
                print(f"❌ Error filtering elements: {e}")
                continue

            if not filtered_elements:
                print(f"⚠️  No elements found with parameter '{parameter_type_name}'")
                continue

            print(f"✅ Found {len(filtered_elements)} element(s) with all values set")

            # Step 5: Calculate sum of parameter values
            print(f"\nCalculating sum of '{parameter_type_name}' values...")
            sum_value = 0
            elements_processed = 0

            try:
                # Sort by nesting level (number of dots in ShortName)
                sorted_elements = sorted(
                    filtered_elements,
                    key=lambda x: x.ShortName.count(".") if hasattr(x, "ShortName") else 0,
                )

                for element in sorted_elements:
                    element_name = (
                        element.ShortName if hasattr(element, "ShortName") else element.Name
                    )

                    # Get matching parameters
                    matching_params = [
                        p
                        for p in (element.NestedParameter or [])
                        if p.AssociatedParameter.ParameterType.Name == parameter_type_name
                    ]

                    for parameter in matching_params:
                        try:
                            value = int(parameter.ActualValue)
                            sum_value += value
                            elements_processed += 1
                            print(f"   {element_name}: {value}")
                        except (ValueError, TypeError) as e:
                            print(f"   ⚠️  Could not parse value for {element_name}: {e}")
                            continue

            except Exception as e:
                print(f"❌ Error calculating sum: {e}")
                continue

            if elements_processed == 0:
                print("⚠️  No valid parameter values found")
                continue

            print(f"✅ Sum calculated: {sum_value} (from {elements_processed} element(s))")

            # Step 6: Prepare transaction and update parameters
            print(f"\nPreparing transaction to update parameters...")
            try:
                cloned_iteration, transaction = prepareTransaction(iteration)
            except InvalidParametersException as e:
                print(f"❌ Error preparing transaction: {e}")
                continue

            try:
                # Clone and update top element parameter
                if not hasattr(cloned_iteration, "TopElement") or not cloned_iteration.TopElement:
                    print("⚠️  No TopElement found in iteration")
                    continue

                top_element = cloned_iteration.TopElement

                if not hasattr(top_element, "Parameter") or not top_element.Parameter:
                    print("⚠️  No parameters found in TopElement")
                    continue

                parameter = top_element.Parameter[0].Clone(True)
                transaction.CreateOrUpdate(parameter)

                print(f"✅ Parameter cloned and added to transaction")

                # Update value sets with computed values
                state_index = 1
                value_sets_updated = 0

                for value_set in parameter.ValueSet or []:
                    try:
                        computed_value = str(sum_value / state_index)

                        logger.debug(f"Setting value for state {state_index}: {computed_value}")
                        logger.debug(
                            f"ParameterSwitchKind type: {type(ParameterSwitchKind.COMPUTED)}"
                        )

                        updated_value_set = setValue(
                            value_set, ParameterSwitchKind.COMPUTED, [computed_value]
                        )
                        transaction.CreateOrUpdate(updated_value_set)
                        value_sets_updated += 1
                        print(f"   ValueSet[{state_index}]: {computed_value}")
                    except (InvalidParametersException, ValueError) as e:
                        print(f"   ⚠️  Error setting value for state {state_index}: {e}")
                        logger.debug(f"Exception details: {type(e).__name__}", exc_info=True)
                        continue
                    except Exception as e:
                        print(f"   ⚠️  Unexpected error setting value for state {state_index}: {e}")
                        import traceback

                        logger.debug(f"Exception details: {traceback.format_exc()}")
                        continue
                    finally:
                        state_index += 1

                if value_sets_updated == 0:
                    print("⚠️  No value sets were updated")
                    continue

                print(f"✅ Updated {value_sets_updated} value set(s)")

            except Exception as e:
                print(f"❌ Error updating parameters: {e}")
                import traceback

                traceback.print_exc()
                continue

            # Step 7: Write transaction to server
            print(f"\nWriting transaction to server...")
            try:
                write_result = session.write(transaction)
            except SessionException as e:
                print(f"❌ Error writing transaction: {e}")
                continue

            # Check write result
            if isinstance(write_result, str):
                print(f"❌ Write operation failed: {write_result}")
            else:
                print("✅ Write operation successful")

    # Cleanup
    print(f"\n{'='*60}")
    print("Closing session...")
    close_result = session.close()

    if close_result is not None:
        print(f"⚠️  Warning during session close: {close_result}")
    else:
        print("✅ Session closed successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
