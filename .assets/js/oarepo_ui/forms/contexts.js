import React from 'react'

export const FormConfigContext = React.createContext()

export const useFormConfig = () => {
    const context = React.useContext(FormConfigContext)
    if (!context) {
        throw new Error('useFormConfig must be used inside FormConfigContext.Provider')
    }
}

export const FormConfigProvider = ({children, value}) => {
    return <FormConfigContext.Provider value={value}>{children}</FormConfigContext.Provider>
}
