package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"simple-distributed-systems-with-go/registration"
)

func main() {
	registration.SetupRegistrationService()
	http.Handle("/services", &registration.RegisterService{})

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	var srv http.Server
	srv.Addr = registration.ServerPort

	go func() {
		fmt.Printf("starting registration service at %v\n", registration.ServiceURL)
		log.Println(srv.ListenAndServe())
		cancel()
	}()

	go func() {
		fmt.Println("registration service started. press any key to stop.")
		var s string
		fmt.Scanln(&s)
		srv.Shutdown(ctx)
		cancel()
	}()
	<-ctx.Done()
	fmt.Println("shutting down registration service.")
}
