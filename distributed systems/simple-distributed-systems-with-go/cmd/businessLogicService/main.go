package main

import (
	"context"
	"fmt"
	stlog "log"
	"simple-distributed-systems-with-go/businessLogic"
	"simple-distributed-systems-with-go/log"
	"simple-distributed-systems-with-go/registration"
	"simple-distributed-systems-with-go/service"
)

func main() {
	host, port := "localhost", "6000"
	serviceAddress := fmt.Sprintf("http://%s:%s", host, port)

	r := registration.Registration{
		ServiceName:       registration.BusinessLogicService,
		ServiceURL:        serviceAddress,
		DependentServices: []registration.ServiceName{registration.LogService},
		ServiceUpdateUrl:  serviceAddress + "/services",
		HeartbeatUrl:      serviceAddress + "/heartbeat",
	}

	ctx, err := service.Start(
		context.Background(),
		host,
		port,
		r,
		businessLogic.RegisterHandlers,
	)

	if err != nil {
		stlog.Fatal(err)
	}

	if logProvider, err := registration.GerProvider(registration.LogService); err == nil {
		fmt.Printf("logging service found at: %v\n", logProvider)
		log.SetClientLogger(logProvider, r.ServiceName)
	}
	<-ctx.Done()
	fmt.Println("shutting key value service")
}
