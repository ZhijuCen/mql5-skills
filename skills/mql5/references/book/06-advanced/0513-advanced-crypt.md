# Cryptography

Algo trading appeared at the cross-section of exchange trading and information technology, allowing, on the one hand, to connect more and more new markets to work, and on the other hand, to expand the functionality of trading platforms. One technological trend that has made its way into most areas of activity, including the arsenals of traders, is cryptography, or, more generally, information security.

MQL5 provides functions for encrypting, hashing, and compressing data: CryptEncode and CryptDecode. We have already used them in some of the examples in the book: in the script EnvSignature.mq5 ([Binding a program to runtime properties](/en/book/common/environment/env_signature)) and the service ServiceAccount.mq5 ([Services](/en/book/applications/script_service/services)).

In this chapter, we will discuss these functions in more detail. However, before proceeding directly to their description, let's review the information transformation methods: this direction of programming is very extensive, and MQL5 supports only a part of the standards. This list will probably be expanded in the future, but for now, if you don't find the required encryption method in the help, try to find a ready-made implementation on mql5.com website (in the article sections or in the source code database).
