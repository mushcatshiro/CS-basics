package main

import (
	"context"
	"fmt"
	stlog "log"
	"simple-distributed-systems-with-go/log"
	"simple-distributed-systems-with-go/registration"
	"simple-distributed-systems-with-go/service"
)

func main() {
	log.Run("./distributed.log")
	host, port := "localhost", "3000"
	serviceAddress := fmt.Sprintf("http://%s:%s", host, port)
	r := registration.Registration{
		ServiceName:       registration.LogService,
		ServiceURL:        serviceAddress,
		DependentServices: make([]registration.ServiceName, 0),
		ServiceUpdateUrl:  serviceAddress + "/services",
		HeartbeatUrl:      serviceAddress + "/heartbeat",
	}
	ctx, err := service.Start(
		context.Background(),
		host,
		port,
		r,
		log.RegisterHandlers,
	)

	if err != nil {
		stlog.Fatalln(err)
	}
	<-ctx.Done()

	fmt.Println("shutting down log service")
}
