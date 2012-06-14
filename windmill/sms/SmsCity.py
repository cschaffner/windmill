"""
=============================================================================
@file: SmsCity.py
@author: SMScity International B.V.
@version: v0.1 - 2010-06-29
@requires: This class requires that you have Python 2.x or higher installed

@note: For more information visit http://business.smscity.com/api/explain/
=============================================================================
"""

# For handeling a specific date/time for sending a message
from datetime import \
    datetime

# For reading/parsing the XML response
from xml.dom.minidom import parseString

# For sending and encoding an HTTP POSTS
import httplib
import urllib

class SmsCity:
    """ SmsCity Class which will handle sending messages to the SMScity website using the SMScity API """

    # @var sender: mixed: Can be an number (16 numbers) or an text (11 characters)
    sender = ''

    # @var destination: list: Holds one or more recipients
    destination = []

    # @var reference: integer: The reference to identify delivery reports using this reference and the destinations
    reference = None

    # @var responseType: string: Could be XML, PLAIN or SIMPLE. Determines which kind of response the server will send
    responseType = 'XML'

    # @var timestamp: datetime: Holds the timestamp to schedule a message, instead of sending it now
    timestamp = None

    # @var httpResponseStatus: string: Will hold the response status returned by the SMScity server
    httpResponseStatus = ''

    # @var httpResponseReason: string: Will hold the response reason returned by the SMScity server
    httpResponseReason = ''

    # @var httpResponseData: string: Will hold the full response data returned by the SMScity server nothing is parsed from this string
    httpResponseData = ''

    # @var xmlResponseData: documentElement: The XML data parsed by the minidom
    xmlResponseData = None


    def __init__(self, username, password):
        """
        This constructor sets both the username and password
        @param username: string The username of the SMScity account
        @param password: string The password of the SMScity account
        """
        self.username = username
        self.password = password


    def addDestination(self, destination):
        """
        Adds an MSISDN to the destination array
        @param destination: integer The destination MSISDN (Mobile number)
        """
        self.destination.append(destination)

    
    def setDestination(self, destination):
        """
        Sets an MSISDN to the destination array after clearing it
        @param destination: integer The destination MSISDN (Mobile number)
        """
        self.destination = []
        self.destination.append(destination)



    def setReference(self, reference):
        """
        Sets the reference linked to the MSISDN so the correct status can be retrieved later.
        @param reference: integer An unique reference so delivery reports can be linked to the correct message and MSISDN
        """
        self.reference = reference


    def setSender(self, sender):
        """
        Sets the sender. This can be an MSISDN (Mobile number) or an Text.
        When it is only numbers it can be 16 numbers, when it is text, it can only be 11 characters long.
        @param sender: mixed The sender of the message which the recipient will see.
        """
        self.sender = sender


    def setTimestamp(self, scheduleDateTime):
        """
        Sets the date and time when the message should be sent.
        NOTE: Our server uses the CET (UTC +1), CEST (UTC +2), Europe/Amsterdam as time reference
        @param scheduleDateTime: datetime An datetime object with at least year, month, day, hour and minute.
        """
        if isinstance(scheduleDateTime, datetime):
            # Our API needs the timestamp in YearMonthDayHourMinute so we convert it to this format
            self.timestamp = scheduleDateTime.strftime('%Y%m%d%H%M')


    def setResponseType(self, responseType):
        """
        Sets the response type to be used for retrieveing the response in specific manner.
        You can change the response type to anything which is in the API Documentation.
        @param responseType: string Could be XML, PLAIN or SIMPLE (Default: XML)
        """
        self.responseType = responseType


    def sendSms(self, message):
        """
        Will actualy send the given message to the destinations given using addDestination()
        @param message: string The message which should be sent to the added destinations.
        """
        # We need all the destinations comma separated
        destinations = ','.join(self.destination)

        # Set the default parameters that needs to be sent
        params = {'username': self.username,
                  'password': self.password,
                  'destination': destinations,
                  'responsetype': self.responseType,
                  'sender': self.sender,
                  'body': message
                 }

        # If there is a reference set, add it to the parameters
        if not self.reference == None:
            params.update({'reference': self.reference})

        # If there is a timestamp set, add it to the parameters
        if not self.timestamp == None:
            params.update({'timestamp': self.timestamp})

        # urlencode all the paramters
        postParams = urllib.urlencode(params)

        # Set the HTTP Headers
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        httpConnection = httplib.HTTPConnection('api.smscity.com')
        httpConnection.request('POST', '/gateway/sms.php', postParams, headers)
        httpResponse = httpConnection.getresponse()

        # Read the response data/info
        self.httpResponseStatus = httpResponse.status
        self.httpResponseReason = httpResponse.reason
        self.httpResponseData = httpResponse.read()

        # Close the HTTP connection
        httpConnection.close()

        if self.responseType == 'XML':
            self.xmlResponseData = parseString(self.httpResponseData).documentElement


    def getResponseCode(self):
        """
        Will return the response code which is returned after sending the the message.
        When the responseType is set to XML there can could be more data to be retrieved.
        @return: string The response code
        """
        if not self.xmlResponseData == None:
            responseCodeTag = self.xmlResponseData.getElementsByTagName('responseCode')
            if responseCodeTag.length > 0:
                return responseCodeTag[0].firstChild.data
            else:
                return ''
        else:
            return self.httpResponseData


    def getResponseMessage(self):
        """
        Will return the response message.
        This is only available when using PLAIN or XML, when using SIMPLE, it will return the responseCode
        @return: string The response message
        """
        if not self.xmlResponseData == None:
            responseMessageTag = self.xmlResponseData.getElementsByTagName('responseMessage')
            if responseMessageTag.length > 0:
                return responseMessageTag[0].firstChild.data
            else:
                return ''
        else:
            return self.httpResponseData


    def getCreditBalance(self):
        """
        Will return the current credit balance left after sending the messages.
        This is only available when using XML as a responseType, all others will always return 0!
        @return: integer The current credit balance after sending the message. (0 when responseType is not XML or an error occurred)
        """
        if not self.xmlResponseData == None:
            creditsTag = self.xmlResponseData.getElementsByTagName('credits')
            if creditsTag.length > 0:
                return creditsTag[0].firstChild.data

        # Return 0 in all other cases, because we don't know the current credits balance
        return 0

