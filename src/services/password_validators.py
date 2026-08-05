from passguard import PasswordPolicy, PasswordValidator
from passguard.rules.character import SymbolRule

policy = PasswordPolicy.default()
policy.remove_rule(SymbolRule)

password_validator = PasswordValidator(policy)
