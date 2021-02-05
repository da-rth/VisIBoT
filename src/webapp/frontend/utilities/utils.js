export function serverColor(serverType) {
  switch (serverType) {
    case "Bot":
      return "#51a1ba"
    case "Malicious Bot":
      return "#46b8a2"
    case "Payload Server":
      return "#ff9033"
    case "Report Server":
      return "#895dda"
    case "C2 Server":
      return "#da4e5b"
    case "P2P Node":
      return "#7488c3"
    default:
      return "#919191"
  }
}

export function serverActivity(serverType) {
  switch (serverType) {
    case "Malicious Bot":
      return "Malicious Botnet Activity"
    case "Payload Server":
      return "Payload Server Activity"
    case "Report Server":
      return "Report Server Activity"
    case "C2 Server":
      return "Command and Control Activity"
    case "P2P Node":
      return "Peer-to-peer Activity"
    default:
      return "Bot-like Activity"
  }
}

export function formatDate(vm, date) {
  return vm.$moment(date).format("DD-MM-YYYY H:mm:ss z")
}
