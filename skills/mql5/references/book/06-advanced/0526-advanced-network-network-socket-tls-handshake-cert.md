# Preparing a secure socket connection

To transfer a socket connection to a protected state and check it, MQL6 provides the following functions: SocketTlsHandshake and SocketTlsCertificate, respectively. As a rule, we do not need to "manually" enable protection by calling SocketTlsHandshake if the connection is established on port 443. The fact is that it is standard for HTTPS (TLS).

Protection is based on encryption of the data flow between the client and the server, for which a pair of asymmetric keys is initially used: public and private. We have already touched on this topic in the section [Overview of available information transformation methods](/en/book/advanced/crypt/crypt_overview). Every decent site acquires a digital certificate from one of the certification authorities (CAs) trusted by the network community. The certificate contains the site's public key and is digitally signed by the center. Browsers and other client applications store (or can import) the public keys of CAs and therefore can verify the quality of a particular certificate.

![Establishing a secure TLS connection  
 (picture from the internet)](pics/tls_sequence.png)

Establishing a secure TLS connection   

(picture from the internet)

Further, when preparing a secure connection, the browser or application generates a certain "secret", encrypts it with the site's public key and sends the key to it, and the site decrypts it with the private key which only the site knows. This stage looks more complicated in practice, but as a result, both the client and the server have the encryption key for the current session (connection). This key is used by both participants in the communication to encrypt subsequent requests and responses at one end and decrypt them at the other.

The SocketTlsHandshake function initiates a secure TLS connection with the specified host using the TLS handshake protocol. In this case, the client and the server agree on the connection parameters: the version of the protocol used and the method of data encryption.

bool SocketTlsHandshake(int socket, const string host)

The socket handle and the address of the server with which the connection is established are passed in the function parameters (in fact, this is the same name that was specified in SocketConnect).

Before a secure connection, the program must first establish a regular TCP connection with the host using [SocketConnect](/en/book/advanced/network/network_socket_create_connect).

The function returns true if successful; otherwise, it returns false. In case of an error, code 5274 (ERR_NETSOCKET_HANDSHAKE_FAILED) is written in  _LastError.

The SocketTlsCertificate function gets information about the certificate used to secure the network connection.

int SocketTlsCertificate(int socket, string &subject, string &issuer, string &serial, string &thumbprint, datetime &expiration)

If a secure connection is established for the socket (either after an explicit and successful SocketTlsHandshake call or after connecting via port 443), this function fills in all other reference variables by the socket descriptor with the corresponding information: the name of the certificate owner (subject), certificate issuer name (issuer), serial number (serial), digital fingerprint (thumbprint), and certificate validity period (expiration).

The function returns true in case of successful receipt of information about the certificate or false as a result of an error. The error code is 5275 (ERR_NETSOCKET_NO_CERTIFICATE). This can be used to determine whether the connection opened by the SocketConnect is immediately in protected mode. We will use this in an example in the next section.
