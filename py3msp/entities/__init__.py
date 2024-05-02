from dataclasses import dataclass, field, fields
import datetime
from typing import Union
from pyamf import remoting
from typing import Dict, Any, Optional
from py3msp.enums import MspRequestError

@dataclass
class HashSaltPreset:
    """A preset configuration for hash salt and no ticket value."""
    salt: str = "2zKzokBI4^26#oiP"
    no_ticket_value: str = "XSV7%!5!AX2L8@vn"


@dataclass
class AMFResult:
    """Represents the result of an AMF request."""

    bytes_data: bytes
    status_code: int

    @property
    def content(self) -> Union[list, dict, None]:
        """
        Decodes the bytes_data into a dictionary or list.

        Returns:
            Union[list, dict, None]: Decoded content if successful, otherwise None.
        """
        try:
            return remoting.decode(self.bytes_data)["/1"].body
        except Exception as e:
            return None

    @property
    def code(self) -> Union[int, None]:
        """
        Extracts the 'Code' field from the content.

        Returns:
            Union[int, None]: The code if available, otherwise None.
        """
        if isinstance(self.content, dict):
            return self.content.get('Code')
        return None

    @property
    def rateLimited(self) -> bool:
        """
        Checks if the request is rate limited.

        Returns:
            bool: True if rate limited, False otherwise.
        """
        return self.status_code == 500

    @property
    def error_description(self) -> MspRequestError:
        """
        Retrieves the error description based on the status code.

        Returns:
            MspRequestError: The error description.
        """
        if self.status_code == 500:
            return MspRequestError.RateLimited
        if self.status_code == 400:
            return MspRequestError.BadRequest
        if self.status_code == 200:
            return MspRequestError.OK
        
    @property
    def proxy_error(self) -> bool:
        """
        Checks if the response is a proxy error or a 404 Forbidden error.

        Returns:
            bool: True if it's a proxy error or a 404 Forbidden error, False otherwise.
        """
        return self.status_code == 503
    
    @property
    def error_description_str(self) -> Optional[str]:
        """
        Provides a description of the error, if available.

        Returns:
            Optional[str]: Description of the error, or None if not available.
        """
        if self.code is not None:
            return f"Error code: {self.code}"
        elif self.status_code == 404:
            return "404 Not Found (Forbidden)"
        elif self.status_code == 503:
            return "Proxy not working"
        elif self.proxy_error:
            return f"Proxy Error: {self.status_code}"
        else:
            return None


@dataclass
class Actor:
    ActorId: int = 0
    Level: int = 0
    Name: str = None
    SkinSWF: str = None
    SkinColor: str = None
    NoseId: int = 0
    EyeId: int = 0
    MouthId: int = 0
    Money: int = 0
    EyeColors: str = None
    MouthColors: str = None
    Fame: int = 0
    Fortune: int = 0
    FriendCount: int = 0
    Created: datetime = datetime.datetime.utcnow()
    LastLogin: datetime = datetime.datetime.utcnow()
    Moderator: int = 0
    ProfileDisplays: int =0
    IsExtra: int = 0
    ValueOfGiftsReceived: int = 0
    ValueOfGiftsGiven: int = 0
    NumberOfGiftsGiven: int = 0
    NumberOfGiftsReceived: int = 0
    NumberOfAutographsReceived: int = 0
    NumberOfAutographsGiven: int = 0
    TimeOfLastAutographGiven: datetime = datetime.datetime.utcnow()
    BoyfriendId: int = None
    MembershipPurchasedDate: datetime = datetime.datetime.utcnow()
    MembershipTimeoutDate: datetime = datetime.datetime.utcnow()
    MembershipGiftRecievedDate: datetime = datetime.datetime.utcnow()
    BehaviourStatus: int = 0
    LockedUntil: datetime = datetime.datetime.utcnow()
    LockedText: str = None
    BadWordCount: int = 0
    PurchaseTimeoutDate: datetime = datetime.datetime.utcnow()
    EmailValidated: int = 0
    RetentionStatus: int = 0
    GiftStatus: int = 0
    MarketingNextStepLogins: int = 0
    MarketingStep: int = 0
    TotalVipDays: int = 0
    RecyclePoints: int = 0
    EmailSettings: int = 0
    TimeOfLastAutographGivenStr: datetime = datetime.datetime.utcnow()
    FriendCountVIP: int = 0
    ForceNameChange: int = 0
    CreationRewardStep: int = 0
    CreationRewardLastAwardDate: datetime = datetime.datetime.utcnow()
    NameBeforeDeleted: str = None
    LastTransactionId: int = 0
    AllowCommunication: int = 1
    Diamonds: int = 0
    PopUpStyleId: int = 0
    EyeShadowId: int = 0
    EyeShadowColors: str = None
    RoomLikes: int = 0
    Email: str = None


@dataclass
class NebulaLoginStatus:
    accessToken: Optional[str] = None
    profileId: Optional[str] = None
    refresh_token: Optional[str] = None

@dataclass
class LoginStatus:
    def default_nebula_login_status():
        return NebulaLoginStatus()

    status: str = None
    userType: str = None
    userIp: int = -1
    ticket: str = None
    boughtRespinToday: bool = False
    diamondRespinPrice: int = 0
    fameWheelSpinPrice: int = 0
    wheelDownloadableFameSpins: int = 0
    nebulaLoginStatus: NebulaLoginStatus = field(default_factory=default_nebula_login_status)
    actor: Actor = field(default_factory=Actor)

    @property
    def isLoggedIn(self) -> bool:
        return self.status in {'Success', 'ThirdPartyCreated'}
    
    @property
    def ActorId(self) -> int:
        return int(self.ticket.split(',')[1]) if self.ticket != None else None

@dataclass
class LoginResult:
    loginStatus: LoginStatus = field(default_factory=LoginStatus)


@dataclass
class MSP2ItemTemplate:
    nameResourceIdentifier: str = None
    lookUpId: str = None
    id: str = None
    graphicsResourceIdentifier: str = None
    created = datetime.datetime