# Remove

Removes the first occurrence of the key/value pair from the hash table.

The version that removes a key-value pair based on the generated key-value pair.

```
bool Remove(
   CKeyValuePair<TKeyTValue>*  item     // the key/value pair"
   );

```

The version that removes a key-value pair based on the key.

```
bool Remove(
   TKey  key                            // key
   );

```

Parameters

*item

[in]  The key/value pair.

key

[in]  Key.

Return Value

Returns true on successful, or false otherwise.
