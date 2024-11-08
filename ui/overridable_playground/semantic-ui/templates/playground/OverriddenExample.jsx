import * as React from 'react';

export const OverriddenExample = ({children=null, ...props}) => {
    return <div>
        <h3>This is my OVERRIDDEN React component with original props as:</h3>
        <pre>{JSON.stringify(props)}</pre>
    </div>
}

export default OverriddenExample;