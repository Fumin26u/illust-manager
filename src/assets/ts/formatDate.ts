const formatDatetimeToMySQLString = (datetime: Date): string => {
    const pad = (num: number): string => num.toString().padStart(2, '0')

    const year = datetime.getFullYear()
    const month = pad(datetime.getMonth() + 1)
    const day = pad(datetime.getDate())
    const hours = pad(datetime.getHours())
    const minutes = pad(datetime.getMinutes())
    const seconds = pad(datetime.getSeconds())

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

export const formatUnixTime = (unixTime: number): string => {
    return formatDatetimeToMySQLString(new Date(unixTime))
}

export const formatCurrentTime = (): string => {
    return formatDatetimeToMySQLString(new Date())
}
