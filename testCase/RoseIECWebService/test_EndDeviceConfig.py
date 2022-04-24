# _*_ coding: utf-8 _*_
# @Time      : 2022/3/17 13:52
# @Author    : Jiannan Cao
# @FileName  : EndDeviceConfig.py

test_request = '''<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
	<soap:Body>
		<Request xmlns="http://iec.ch/TC57/2011/schema/message">
			<RequestMessage>
				<Header>
					<Verb>create</Verb>
					<Noun>UsagePointConfig</Noun>
					<Revision>1.0</Revision>
					<Timestamp>2017-09-06T20:35:45.0000012+05:00</Timestamp>
					<Source>MDMS</Source>
					<MessageID>8B3EF3E8-C61C-4C91-BEF0-A1775570656A</MessageID>
					<CorrelationID>8B3EF3E8-C61C-4C91-BEF0-A1775570656A</CorrelationID>
				</Header>
				<Payload>
					<UsagePointConfig xmlns="http://iec.ch/TC57/2011/UsagePointConfig#">
						<UsagePoint>
							<mRID>1234567891</mRID>
							<ConfigurationEvents>
								<createdDateTime> 
2017-09-06T20:35:45.0000012+05:00
</createdDateTime>
							</ConfigurationEvents>
							<Names>
								<NameType>
									<description>this is the description</description>
								</NameType>
							</Names>
							<UsagePointLocation>
								<PositionPoints>
									<xPosition>1.325684</xPosition>
									<yPosition>2.356472</yPosition>
								</PositionPoints>
<mainAddress>
								    <streetDetail>
									   <addressGeneral> chengdu china </addressGeneral>
									</streetDetail>
</mainAddress>
							</UsagePointLocation>
							<Equipments>
								<Names>
									<name>60</name>
								</Names>
							</Equipments>
						</UsagePoint>
						<UsagePoint>
							<mRID>1234567890</mRID>
							<Names>
								<NameType>
									<description>this is the description</description>
								</NameType>
							</Names>
							<UsagePointLocation>
								<PositionPoints>
									<xPosition>1.325684</xPosition>
									<yPosition>2.356472</yPosition>
								</PositionPoints>
<mainAddress>
								    <streetDetail>
									   <addressGeneral> chengdu china </addressGeneral>
									</streetDetail>
</mainAddress>
							</UsagePointLocation>
							<Equipments>
								<Names>
									<name>60</name>
								</Names>
							</Equipments>
						</UsagePoint>
					</UsagePointConfig>
				</Payload>
			</RequestMessage>
		</Request>
	</soap:Body>
</soap:Envelope>
'''
