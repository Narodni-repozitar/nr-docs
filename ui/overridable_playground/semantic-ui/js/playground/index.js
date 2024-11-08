import * as React from 'react'
import ReactDOM from 'react-dom'
import Overridable, { OverridableContext, overrideStore } from 'react-overridable'

const ExampleComp = ({title='Default React component', color='red'}) => {
    return <Overridable id="ExampleComponent.container" cmpTitle={title} cmpColor={color}>
        <>
            <h3 style={{color: color}}>{title}</h3>
        </>
    </Overridable>
}

ReactDOM.render(
  <OverridableContext.Provider value={overrideStore.getAll()}>
      <ExampleComp />
  </OverridableContext.Provider>, document.getElementById('react-example-1'));