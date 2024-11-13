import * as rif from 'react-invenio-forms'

console.log(rif)
export const MyComponentsOverriddenExample = ({children=null, ...props}) => {
    return <div>
        <h3>This is my OVERRIDDEN React component with original props as:</h3>
        <pre>{JSON.stringify(rif)}</pre>
    </div>
};

export default MyComponentsOverriddenExample;