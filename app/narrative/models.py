from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class NarrativeItem:
    """
    Represents one computed figure prepared for narrative generation.
    """

    section: str

    title: str

    value: str

    limit: str

    status: str

    utilization: str | None = None


@dataclass(slots=True, frozen=True)
class NarrativeContext:
    """
    Context passed to the narrative generator.
    """

    fund_name: str

    items: list[NarrativeItem]

@dataclass(slots=True, frozen=True)
class NarrativeResult:
    """
    Result returned by a narrative generator.
    """

    content: str

    model: str

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    total_tokens: int | None = None

# ============================================================ 
# Narrative Firewall 
# ============================================================

@dataclass(slots=True, frozen=True) 
class FirewallIssue: 
    """ Represents one validation issue detected by the Narrative Firewall. """ 
    rule: str 
    message: str 
    expected: str | None = None 
    actual: str | None = None

@dataclass(slots=True) 
class FirewallResult: 
    """ Result produced by the Narrative Firewall. """ 
   
    passed: bool = True 
    issues: list[FirewallIssue] = field( 
        default_factory=list, 
    ) 

    def add_issue( self, *, rule: str, message: str, expected: str | None = None, actual: str | None = None, ) -> None: 
        """ Add a validation issue. """ 
        self.passed = False 
        self.issues.append( 
            FirewallIssue( 
                rule=rule, 
                message=message, 
                expected=expected, 
                actual=actual, 
            ) 
        )