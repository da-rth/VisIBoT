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
      return "#b18873"
    default:
      return "#919191"
  }
}

export function formatDate(vm, date) {
  return vm.$moment(date).format("DD-MM-YYYY H:mm:ss z")
}
