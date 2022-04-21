# -*- coding: UTF-8 -*-

ControlMap = {
    "93": "SNRM",
    "73": "UA",
    "53": "DISC",
    "0F": "DM",
    "10": "AARQ",
    "30": "AARE",
    "32": "GET.request",
    "52": "GET.response",
}

DataType = {
    "0": "null-data",
    "1": "array",
    # The elements of the array are defined in the Attribute or Method description section of a COSEM IC specification.
    "2": "Structure",
    # The elements of the structure are defined in the Attribute or Method description section of a COSEM IC specification.
    "3": "boolean",  # boolean
    "4": "bit-string",  # An ordered sequence of boolean values
    "5": "double-long",  # Integer32
    "6": "double-long-unsigned",  # Unsigned32
    "7": "floating-point",
    "8": "",
    "9": "octet-string",  # An ordered sequence of octets (8 bit bytes)
    "10": "visible-string",  # An ordered sequence of ASCII characters
    "11": "time",
    "12": "utf8-string",  # An ordered sequence of characters encoded as UTF-8
    "13": "bcd",  # binary coded decimal
    "14": "",
    "15": "integer",  # Integer8
    "16": "long",  # Integer16
    "17": "unsigned",  # Unsigned8
    "18": "long-unsigned",  # Unsigned16
    "19": "Compact array",  # Provides an alternative, compact encoding of complex data.
    "20": "long64",  # Integer64
    "21": "long64-unsigned",  # Unsigned64
    "22": "enum",
    # The elements of the enumeration type are defined in theAttribute description or Method description section of a COSEM  IC specification.
    "23": "float32",  # OCTET STRING (SIZE(4))
    "24": "float64",  # OCTET STRING (SIZE(8))
    "25": "date-time",  # OCTET STRING SIZE(12))
    "26": "date",  # OCTET STRING (SIZE(5))
    "27": "time"  # OCTET STRING (SIZE(4))
}

PduClassMap = {
    "60": "AARQApduParser",
    "61": "AAREApduParser",
    "62": "RLRQApduParser",
    "63": "RLREApduParser",
    "01": "InitRequestApduParser",
    "08": "InitResponseApduParser",
}

ConformanceMap = {
    "1": "general-protection",
    "2": "general-block-transfer",
    "3": "read",
    "4": "write",
    "5": "unconfirmed-write",
    "6": "reserved-six",
    "7": "reserved-seven",
    "8": "attribute0-supported-with-set",
    "9": "priority-mgmt-supported",
    "10": "attribute0-supported-with-get",
    "11": "block-transfer-with-get-or-read",
    "12": "block-transfer-with-set-or-write",
    "13": "block-transfer-with-action",
    "14": "multiple-references",
    "15": "information-report",
    "16": "data-notification",
    "17": "access",
    "18": "parameterized-access",
    "19": "get",
    "20": "set",
    "21": "selective-access",
    "22": "event-notification",
    "23": "action",
}

PduMap = {
    # with no ciphering
    "1": "initiateRequest",
    "5": "readRequest",
    "6": "writeRequest",
    "8": "initiateResponse",
    "12": "readResponse",
    "13": "writeResponse",
    "14": "confirmedServiceError",
    "15": "data-notification",
    "22": "unconfirmedWriteRequest",
    "24": "informationReportRequest",

    # with global ciphering
    "33": "glo-initiateRequest",
    "37": "glo-readRequest",
    "38": "glo-writeRequest",
    "40": "glo-initiateResponse",
    "44": "glo-readResponse",
    "45": "glo-writeResponse",
    "46": "glo-confirmedServiceError",
    "54": "glo-unconfirmedWriteRequest",
    "56": "glo-informationReportRequest",

    # with dedicated ciphering
    "65": "ded-initiateRequest",
    "69": "ded-readRequest",
    "70": "ded-writeRequest",
    "72": "ded-initiateResponse",
    "76": "ded-readResponse",
    "77": "ded-writeResponse",
    "78": "ded-confirmedServiceError",
    "86": "ded-unconfirmedWriteRequest",
    "88": "ded-informationReportRequest",

    # ACSE-APDU
    "96": "AARQ",  # 60(H)
    "97": "AARE",  # 61(H)
    "98": "RLRQ",  # 62(H)
    "99": "RLRE",  # 63(H)

    # with no ciphering
    "192": "get-request",
    "193": "set-request",
    "194": "event-notification-request",
    "195": "action-request",
    "196": "get-response",
    "197": "set-response",
    "199": "action-response",

    # with global ciphering
    "200": "glo-get-request",
    "201": "glo-set-request",
    "202": "glo-event-notification-request",
    "203": "glo-action-request",
    "204": "glo-get-response",
    "205": "glo-set-response",
    "207": "glo-action-response",

    # with dedicated ciphering
    "208": "ded-get-request",
    "209": "ded-set-request",
    "210": "ded-event-notification-request",
    "211": "ded-actionRequest",
    "212": "ded-get-response",
    "213": "ded-set-response",
    "215": "ded-action-response",

    # the exception response pdu
    "216": "exception-response",

    # access
    "217": "access-request",
    "218": "access-response",

    # general APDUs
    "219": "general-glo-ciphering",
    "220": "general-ded-ciphering",
    "221": "general-ciphering",
    "223": "general-signing",
    "224": "general-block-transfer",
}

# MechanismMap = {
#     "0"   : "lowest_level_security",
#     "1"   : "low_level_security",
#     "2"   : "high_level_security",
#     "3"   : "high_level_security_md5",
#     "4"   : "high_level_security_sha1",
#     "5"   : "high_level_security_gmac",
#     "6"   : "high_level_security_sha256",
#     "7"   : "high_level_security_ecdsa",
# }

MechanismMap = {
    "1": "LOW_SECURITY",
    "2": "HIGH_SECURITY",
    "3": "HIGH_SECURITY_MD5",
    "4": "HIGH_SECURITY_SHA1",
    "5": "HIGH_SECURITY_GMAC",
    "6": "HIGH_SECURITY_SHA256",
    "7": "HIGH_SECURITY_ECDSA",
}

# ConnectStatus = {
#     "1" : "Connect Ok",
#     "2" : "Com Port Error",
#     "3" : "No Response",
#     "4" : "Hdlc Error",
#     "5" : "Reject",
#     "6" : "Gprs Error",
#     "7" : "Dlms Connect Fail",
#     "8" : "Get Fail"
# }


#  ConnectResult (C#)
ConnectStatus = {
    "0": "Invalid connection, mainly refers to the encryption string is wrong",
    "1": "Connect Ok",
    "2": "Serial port error, mainly refers to the serial port opening failure",
    "3": "NoResponse",
    "4": "HDLC error,  mainly refers to communication link error, including no electricity meter connection, connection communication error, etc",
    "5": "DLMS connection rejection, mainly refers to key error",
    "6": "Gprs connection failed",
    "7": "Dlms connection failure, mainly refers to the failure of public connection and ordinary connection, or the failure of establishing false connection under advanced permissions",
    "8": "GetRequest Fail"
}

# GeneralProtectionTypeEnum = {
#     "glo_ciphering" : GeneralProtection.Service_Specific_Ciphering,
#     "ded_ciphering" : GeneralProtection.Service_Specific_Ciphering,
#     "general_glo_ciphering" : GeneralProtection.General_Glo_Ciphering,
#     "general_ded_ciphering" : GeneralProtection.General_Ded_Ciphering,
#     "general_ciphering" : GeneralProtection.General_Ciphering,
#     "general_ciphering_with_signing" : GeneralProtection.General_Signing,
# }

GeneralProtectionTypeEnum = {
    "glo_ciphering": 0,
    "ded_ciphering": 0,
    "general_glo_ciphering": 1,
    "general_ded_ciphering": 2,
    "general_ciphering": 3,
    "general_ciphering_with_signing": 4,
}

UsageDedicatedKeyEnum = {
    "glo_ciphering": False,
    "ded_ciphering": True,
    "general_ded_ciphering": True,
}

# AccessLevelEnum = {
#     "no" : "No Security",
#     "low" : "Low Security",
#     "high" : "High Security",
# }

# MechanismEnum = {
#     "default" : AlgorithmTypeInHighSecurity.AT_GMAC,
#     "md5" : AlgorithmTypeInHighSecurity.AT_MD5,
#     "sha1" : AlgorithmTypeInHighSecurity.AT_SHA1,
#     "gmac" : AlgorithmTypeInHighSecurity.AT_GMAC,
#     "sha256" : AlgorithmTypeInHighSecurity.AT_SHA256,
#     "ecdsa" : AlgorithmTypeInHighSecurity.AT_ECDSA,
# }


MechanismEnum = {
    "default": 0,
    "md5": 1,
    "sha1": 2,
    "gmac": 3,
    "sha256": 4,
    "ecdsa": 5,
}

SecurityPolicyEnum = {
    "0x00": 0x00,
    "0x10": 0x10,
    "0x20": 0x20,
    "0x30": 0x30,
}

UnitsMap = {
    8: "angle",
    9: "temperature",
    27: "W",
    28: "VA",
    29: "var",
    30: "Wh",
    31: "VAh",
    32: "varh",
    33: "A",
    35: "V",
    44: "Hz",
    45: "1/(Wh)",
    46: "1/(varh)",
    47: "1/(VAh)",
    255: "count",
}

data_access_result = ["ReadWriteDenied", "ObjectUndefined", "OtherReason", "DataBlockNumberInvalid",
                      "TypeUnmatched", "NoLongSetInProgress", "LongSetAborted", "NoLongGetInProgress",
                      "LongGetAborted", "DataBlockUnavailable", "ScopeOfAccessViolated", "ObjectUnavailable",
                      "ObjectClassInconsistent", "TemporaryFailure", "HardwareFault"]

ClassInterfaceMap = {
    '1': 'C1Data',
    '3': 'C3Register',
    '4': 'C4ExtendedRegister',
    '5': 'C5Demand',
    '6': 'C6RegisterActivation',
    '7': 'C7Profile',
    '8': 'C8Clock',
    '9': 'C9Script',
    '11': 'C11SpecialDaysTable',
    '15': 'C15AssociationLN',
    '17': 'C17SAP',
    '18': 'C18ImageTransfer',
    '19': 'C19IECLocalPortSetup',
    '20': 'C20ActivityCalendar',
    '21': 'C21RegisterMonitor',
    '22': 'C22SingleActionSchedule',
    '23': 'C23IECHDLCSetup',
    '29': 'C29AutoConnect',
    '40': 'C40PushSetup',
    '41': 'C41TCPUDPSetup',
    '42': 'C42IPv4Setup',
    '43': 'C43MACAddressSetup',
    '44': 'C44PPPSetup',
    '45': 'C45GPRSModemSetup',
    '47': 'C47GSMDiagnostic',
    '48': 'C48IPv6Setup',
    '64': 'C64SecuritySetup',
    '70': 'C70DisconnectControl',
    '71': 'C71Limiter',
    '72': 'C72MBusClient',
    '74': 'C74MBusMasterPortSetup',
    '90': 'C90G3PLCMACLayerCounters',
    '91': 'C91G3PLCMACSetup',
    '92': 'C92G3PLC6LoWPANAdaptationLayerSetup',
}
