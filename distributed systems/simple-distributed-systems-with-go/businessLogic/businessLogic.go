package businessLogic

import (
	"fmt"
	"sync"
)

type KVStore struct {
	KV    []kv
	mutex *sync.Mutex
}

var KVStoreObj KVStore

func (kvs KVStore) Get(key int) (*kv, error) {
	for i := range kvs.KV {
		if kvs.KV[i].key == key {
			return &kvs.KV[i], nil // note if we are returning nil then use pointers
		}
	}
	return nil, fmt.Errorf("key %v is not found on server", key)
}

func (kvs KVStore) Put(key, value int) (*kv, error) {
	kvs.mutex.Lock()
	defer kvs.mutex.Unlock()
	nkv := kv{key, value}
	for i := range kvs.KV {
		if kvs.KV[i].key == key {
			return nil, fmt.Errorf("key %v already exists in key value store", key)
		}
	}
	kvs.KV = append(kvs.KV, nkv)
	return &kvs.KV[len(kvs.KV)-1], nil
}

func (kvs KVStore) Delete(key int) error {
	for i := range kvs.KV {
		if kvs.KV[i].key == key {
			kvs.KV = append(kvs.KV[:i], kvs.KV[i:]...)
			return nil
		}
	}
	return fmt.Errorf("key %v not found in key value store", key)
}

type kv struct {
	key   int
	value int
}
