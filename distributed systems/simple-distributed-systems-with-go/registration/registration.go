package registration

type Registration struct {
	ServiceName       ServiceName
	ServiceURL        string
	DependentServices []ServiceName
	ServiceUpdateUrl  string
	HeartbeatUrl      string
}

type ServiceName string

const (
	LogService           = ServiceName("LogService")
	BusinessLogicService = ServiceName("BusinessLogicService")
)

type patchEntry struct {
	Name ServiceName
	URL  string
}

type patch struct {
	Added   []patchEntry
	Removed []patchEntry
}
