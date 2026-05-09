def is_valid_amount(amount):
    """Returns True if the amount is a positive number, False otherwise."""
    return isinstance(amount, (int, float)) and amount > 0


def process_deposit(balance, amount):
    """
    Validates the amount, applies a 0.5% processing fee, 
    and returns the new balance or an error message.
    """
    if not is_valid_amount(amount):
        return "Error: Deposit amount must be a positive number."
    
    fee = amount * 0.005
    net_deposit = amount - fee
    new_balance = balance + net_deposit
    return new_balance


def process_withdrawal(balance, amount, minimum_balance=5000):
    """
    Validates amount and checks for sufficient funds above the minimum balance.
    Returns the new balance or an error message.
    """
    if not is_valid_amount(amount):
        return "Error: Withdrawal amount must be a positive number."
    
    if (balance - amount) < minimum_balance:
        return f"Error: Insufficient funds. A minimum balance of ₦{minimum_balance:,.2f} must be maintained."
    
    new_balance = balance - amount
    return new_balance


def print_receipt(holder, transaction_type, amount, old_balance, new_balance):
    """Prints a formatted transaction receipt using f-strings."""
    print("\n" + "="*30)
    print("      TRANSACTION RECEIPT")
    print("="*30)
    print(f"Account Holder: {holder}")
    print(f"Transaction:    {transaction_type.capitalize()}")
    print(f"Amount:         ₦{amount:,.2f}")
    print(f"Old Balance:    ₦{old_balance:,.2f}")
    print(f"New Balance:    ₦{new_balance:,.2f}")
    print("="*30 + "\n")


def get_account_summary(holder, balance):
    """Returns a formatted summary string of the account state."""
    return f"FINAL SUMMARY | Holder: {holder} | Current Balance: ₦{balance:,.2f}"


if __name__ == "__main__":
    # Initial Configuration
    account_holder = "John Doe"
    current_balance = 50000.00

    print(f"Welcome to the Bank, {account_holder}!")
    print(f"Your current balance is: ₦{current_balance:,.2f}")
    
    choice = input("Would you like to (D)eposit or (W)ithdraw? ").strip().upper()

    if choice in ['D', 'W']:
        try:
            user_amount = float(input("Enter the amount: ₦"))
            old_bal = current_balance
            
            if choice == 'D':
                result = process_deposit(current_balance, user_amount)
                trans_type = "Deposit (0.5% fee applied)"
            else:
                result = process_withdrawal(current_balance, user_amount)
                trans_type = "Withdrawal"

            # Check if result is a number (success) or string (error)
            if isinstance(result, (int, float)):
                current_balance = result
                print_receipt(account_holder, trans_type, user_amount, old_bal, current_balance)
            else:
                print(f"\n{result}")

        except ValueError:
            print("\nError: Please enter a valid numerical amount.")
    else:
        print("\nInvalid choice. Please restart and select 'D' or 'W'.")

    # Show Final Summary
    print(get_account_summary(account_holder, current_balance))
