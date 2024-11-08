export const OverridenExample = ({children, ...props}) => {
    return <div>
        <h3>This is my OVERRIDDEN React component with original props:</h3>
        <pre>{JSON.stringify(props)}</pre>
        {children}
    </div>
}

export default OverridenExample;