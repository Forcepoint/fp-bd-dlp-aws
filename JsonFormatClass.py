class Compliance:
    def __init__(self, Status=None):
        self.Status = Status


class Malware:
    def __init__(self, Name=None, Path=None, State=None, Type=None):
        self.Name = Name
        self.Path = Path
        self.State = State
        self.Type = Type


class Network:
    def __init__(self, DestinationDomain=None, DestinationIpV4=None, DestinationIpV6=None, DestinationPort=None,
                 Direction=None, Protocol=None, SourceDomain=None, SourceIpV4=None, SourceIpV6=None, SourceMac=None,
                 SourcePort=None):
        self.DestinationDomain = DestinationDomain
        self.DestinationIpV4 = DestinationIpV4
        self.DestinationIpV6 = DestinationIpV6
        self.DestinationPort = DestinationPort
        self.Direction = Direction
        self.Protocol = Protocol
        self.SourceDomain = SourceDomain
        self.SourceIpV4 = SourceIpV4
        self.SourceIpV6 = SourceIpV6
        self.SourceMac = SourceMac
        self.SourcePort = SourcePort


class Note:
    def __init__(self, Text=None, UpdatedAt=None, UpdatedBy=None):
        self.Text = Text
        self.UpdatedAt = UpdatedAt
        self.UpdatedBy = UpdatedBy


class Process:
    def __init__(self, LaunchedAt=None, Name=None, ParentPid=None, Path=None, Pid=None, TerminatedAt=None):
        self.LaunchedAt = LaunchedAt
        self.Name = Name
        self.ParentPid = ParentPid
        self.Path = Path
        self.Pid = Pid
        self.TerminatedAt = TerminatedAt


class ProductFields:
    def __init__(self, string=None):
        self.string = string


class RelatedFinding:
    def __init__(self, Id=None, ProductArn=None):
        self.Id = Id
        self.ProductArn = ProductArn


class Recommendation:
    def __init__(self, Text=None, Url=None):
        self.Text = Text
        self.Url = Url


class Remediation:
    def __init__(self, Recommendation=None):
        self.Recommendation = Recommendation


class AwsEc2Instance:
    def __init__(self, IamInstanceProfileArn=None, ImageId=None, IpV4Addresses=None, IpV6Addresses=None, KeyName=None,
                 LaunchedAt=None, SubnetId=None, Type=None, VpcId=None):
        self.IamInstanceProfileArn = IamInstanceProfileArn
        self.ImageId = ImageId
        self.IpV4Addresses = IpV4Addresses
        self.IpV6Addresses = IpV6Addresses
        self.KeyName = KeyName
        self.LaunchedAt = LaunchedAt
        self.SubnetId = SubnetId
        self.Type = Type
        self.VpcId = VpcId


class AwsIamAccessKey:
    def __init__(self, CreatedAt=None, Status=None, UserName=None):
        self.CreatedAt = CreatedAt
        self.Status = Status
        self.UserName = UserName


class AwsS3Bucket:
    def __init__(self, OwnerId=None, OwnerName=None):
        self.OwnerId = OwnerId
        self.OwnerName = OwnerName


class Container:
    def __init__(self, ImageId=None, ImageName=None, LaunchedAt=None, Name=None):
        self.ImageId = ImageId
        self.ImageName = ImageName
        self.LaunchedAt = LaunchedAt
        self.Name = Name


class Details:
    def __init__(self, AwsEc2Instance=None, AwsIamAccessKey=None, AwsS3Bucket=None, Container=None, Other=None):
        self.AwsEc2Instance = AwsEc2Instance
        self.AwsIamAccessKey = AwsIamAccessKey
        self.AwsS3Bucket = AwsS3Bucket
        self.Container = Container
        self.Other = Other


class Resource:
    def __init__(self, Details=None, Id=None, Partition=None, Region=None, Tags=None, Type=None):
        self.Details = Details
        self.Id = Id
        self.Partition = Partition
        self.Region = Region
        self.Tags = Tags
        self.Type = Type


class Severity:
    def __init__(self, Normalized=None, Product=None, Label=None):
        self.Normalized = Normalized
        self.Product = Product
        self.Label = Label


class ThreatIntelIndicator:
    def __init__(self, Category=None, LastObservedAt=None, Source=None, SourceUrl=None, Type=None, Value=None):
        self.Category = Category
        self.LastObservedAt = LastObservedAt
        self.Source = Source
        self.SourceUrl = SourceUrl
        self.Type = Type
        self.Value = Value


class UserDefinedFields:
    def __init__(self, SourceRuleName=None, SourceEmail=None, SourceUsername=None, SourceFullName=None,
                 SourceLoginName=None, SourceExtraData=None,
                 SourceHostname=None, SourceDestinations=None):
        self.SourceRuleName = SourceRuleName
        self.SourceEmail = SourceEmail
        self.SourceUsername = SourceUsername
        self.SourceFullName = SourceFullName
        self.SourceLoginName = SourceLoginName
        self.SourceExtraData = SourceExtraData
        self.SourceHostname = SourceHostname
        self.SourceDestinations = SourceDestinations


class Finding:
    def __init__(self, AwsAccountId=None, Compliance=None, Confidence=None, CreatedAt=None, Criticality=None,
                 Description=None, FirstObservedAt=None, GeneratorId=None, Id=None, LastObservedAt=None, Malware=None,
                 Network=None, Note=None, Process=None, ProductArn=None, ProductFields=None, RecordState=None,
                 RelatedFindings=None, Remediation=None, Resources=None, SchemaVersion=None, Severity=None,
                 SourceUrl=None, ThreatIntelIndicators=None, Title=None, Types=None, UpdatedAt=None,
                 UserDefinedFields=None, VerificationState=None, WorkflowState=None):
        self.AwsAccountId = AwsAccountId
        self.Compliance = Compliance
        self.Confidence = Confidence
        self.CreatedAt = CreatedAt
        self.Criticality = Criticality
        self.Description = Description
        self.FirstObservedAt = FirstObservedAt
        self.GeneratorId = GeneratorId
        self.Id = Id
        self.LastObservedAt = LastObservedAt
        self.Malware = Malware
        self.Network = Network
        self.Note = Note
        self.Process = Process
        self.ProductArn = ProductArn
        self.ProductFields = ProductFields
        self.RecordState = RecordState
        self.RelatedFindings = RelatedFindings
        self.Remediation = Remediation
        self.Resources = Resources
        self.SchemaVersion = SchemaVersion
        self.Severity = Severity
        self.SourceUrl = SourceUrl
        self.ThreatIntelIndicators = ThreatIntelIndicators
        self.Title = Title
        self.Types = Types
        self.UpdatedAt = UpdatedAt
        self.UserDefinedFields = UserDefinedFields
        self.VerificationState = VerificationState
        self.WorkflowState = WorkflowState


class JsonFormatClass:
    def __init__(self, Finding=None):
        self.Finding = Finding
