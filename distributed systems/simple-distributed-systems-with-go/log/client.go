package log

import (
	"bytes"
	"fmt"
	stlog "log"
	"net/http"
	"simple-distributed-systems-with-go/registration"
)

func SetClientLogger(serviceURL string, clientService registration.ServiceName) {
	stlog.SetPrefix(fmt.Sprintf("[%v] - ", clientService))
	stlog.SetFlags(0)
	stlog.SetOutput(&clientLogger{url: serviceURL})
}

type clientLogger struct {
	url string
}

func (cl clientLogger) Write(data []byte) (int, error) {
	b := bytes.NewBuffer([]byte(data))
	res, err := http.Post(cl.url+"/log", "text/plain", b)
	if err != nil {
		return 0, err
	}
	if res.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("failed to send log message. log service responded with status code %d", res.StatusCode)
	}
	return len(data), nil
}
