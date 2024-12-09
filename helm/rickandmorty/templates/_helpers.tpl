{{- define "rickandmorty.name" -}}
{{ .Chart.Name }}
{{- end -}}

{{- define "rickandmorty.fullname" -}}
{{ include "rickandmorty.name" . }}-{{ .Release.Name }}
{{- end -}}
