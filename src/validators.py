from passguard.rules.character import SymbolRule
from passguard.integrations.pydantic import PasswordField
from passguard import PasswordPolicy


policy = PasswordPolicy.default()
policy.remove_rule(SymbolRule)

password_validator = PasswordField.make_validator(
    policy,
    context_fields=['email', 'first_name', 'last_name']
)