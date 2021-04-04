[TOC]

# gRPC

client and server.

## client

calls directly a method on **server application** on a different machine as if it were a local object to create distributed application and services. so we first need to define methods that can be called remotely with parameters and return types. client has a server that provides the same methods as the server.

## server

implements this interface and runs a gRPC server to handle client calls.

## protocol buffers / protobuf

the default mechanism of serializing data (json also can be used). protobuf documents has a `.proto` extension. protobuf is structured as messages, where each message is a small logical record of information containing a series of name-value pairs called fields.

```protobuf
message person {
	string name = 1; // field numbers are used to identify fields in binary format and should not be changes when used
	optional int32 id = 2; 
	bool has_hair = 3 [default = false];
}
```

we then use protobuf compiler `protoc` to generate data access class in the preferred language (python). it provides simple accessors for each field, eg `name()` and `set_name()` and methods to serialize and parse the whole structure to raw bytes.

gRPC services are defined in ordinary proto files, with RPC method parameters and return type specified as protobuf message.

```protobuf
service Greeter {
	rpc SayHello(HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
	required string name = 1; // required is forever
}

message HelloReply {
	string reply = 1;
}
```

`protoc` with special gRPC plugin generates code from proto files including client and server code as well as regular protobuf code for populating, serializing and retrieving message types.

### service method

- unary
- stream (client / server)
- bidirectional streaming

add `stream` for the message that needs streaming

## using API

1. generate a `.proto` file
2. compile to get server and client side code
3. implement corresponding API in server side
4. call from client

### more on item 3

server side we need to implement methods declard by the service and runs a gRPC server to handle client calls. a gRPC infrastructure decodes incoming requets, executes services methods, and encodes service responses.

### more on item 4

client side has a local object known as stub / client tha implements same methods as the service. then client calls those methods as if there are local, by wrapping the parameters for the call in appropriate protobuf message. gRPC looks after sending the request to the server and return the server protobuf response.