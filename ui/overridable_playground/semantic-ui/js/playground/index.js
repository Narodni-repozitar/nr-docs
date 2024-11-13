import * as React from 'react'
import ReactDOM from 'react-dom'
import Overridable, { OverridableContext, overrideStore } from 'react-overridable'
import * as my from  './mycomponents'

const ExampleComp = ({title='Default React component', color='red'}) => {
    return <Overridable id="ExampleComponent.container" cmpTitle={title} cmpColor={color} my={my}>
        <>
            <h3 style={{color: color}}>{title}</h3>
        </>
    </Overridable>
}


const OtherExampleComp = ({title='Default React component', color='red'}) => {
    return <Overridable id="OtherExampleComponent.container" cmpTitle={title} cmpColor={color}>
        <>
            <h3 style={{color: color}}>{title}</h3>
        </>
    </Overridable>
}


ReactDOM.render(
  <OverridableContext.Provider value={overrideStore.getAll()}>
      <ExampleComp />
      <OtherExampleComp />
  </OverridableContext.Provider>, document.getElementById('react-example'));