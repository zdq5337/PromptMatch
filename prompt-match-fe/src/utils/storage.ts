const parseJSON = (value: string) => {
  try {
    return value === 'undefined' ? undefined : JSON.parse(value ?? '')
  } catch (error) {
    return undefined
  }
}
export default {
  set(
    key: string,
    value: string | object,
    typeOfStorage: 'localStorage' | 'sessionStorage' = 'localStorage'
  ) {
    window[typeOfStorage].setItem(key, JSON.stringify(value))
  },
  get(key: string) {
    try {
      const item = window.localStorage.getItem(key) || window.sessionStorage.getItem(key)
      return item ? parseJSON(item) : null
    } catch (error) {
      return null
    }
  },
  remove(key: string) {
    window.localStorage.removeItem(key)
    window.sessionStorage.removeItem(key)
  }
}
