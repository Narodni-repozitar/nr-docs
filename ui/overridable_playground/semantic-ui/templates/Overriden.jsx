export const MyComponent = ({children, ...props}) => {
    return <div>
        <h3>This is my OVERRIDDEN React component</h3>
        {children}
    </div>
}

export default MyComponent;