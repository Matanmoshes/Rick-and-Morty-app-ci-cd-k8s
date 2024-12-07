{{- define "rickandmorty.name" -}}
{{ include "chart.name" . }}
{{- end -}}

{{- define "rickandmorty.fullname" -}}
{{ include "rickandmorty.name" . }}-{{ .Release.Name }}
{{- end -}}
