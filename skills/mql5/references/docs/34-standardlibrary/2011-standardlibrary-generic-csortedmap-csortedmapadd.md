# Add

Adds a key/value pair to the hash table.

A version that adds a generated key/value pair.

```
bool Add(
   CKeyValuePair<TKeyTValue>*  pair     // the key/value pair
   );

```

A version that adds a new key/value pair with the specified key and value.

```
bool Add(
   TKey    key,                         // key
   TValue  value                        // value
   );

```

Parameters

*pair

[in]  The key/value pair.

key

[in]  Key.

value

[in]  Value.

Return Value

Returns true on successful, or false otherwise.
