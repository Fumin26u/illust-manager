export const extractPath = (
    fullPath: string,
    target: string,
    isContainTarget = true
): string | null => {
    const index = fullPath.indexOf(target)
    if (index !== -1) {
        return isContainTarget
            ? fullPath.substring(index)
            : fullPath.substring(index + target.length)
    }

    return fullPath ?? null
}
