package businessLogic

import (
	"encoding/json"
	"log"
	"net/http"
)

func RegisterHandlers() {
	handler := new(businessLogicHandler)
	http.Handle("/kvstore", handler)
}

type businessLogicHandler struct{}

func (blh businessLogicHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		dec := json.NewDecoder(r.Body)
		var k kv
		err := dec.Decode(&k)
		if err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		kv, err := KVStoreObj.Put(k.key, k.value)
		if err != nil {
			log.Println(err)
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		resp, err := json.Marshal(kv)
		w.WriteHeader(http.StatusOK)
		w.Write(resp)
		return
	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}
}
