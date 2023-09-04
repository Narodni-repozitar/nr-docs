import { useState } from "react";

export const useHighlightState = () => {
  const [highlightedStates, setHighlightedStates] = useState([]);

  const handleHover = (index) => {
    const updatedStates = [...highlightedStates];
    updatedStates[index] = true;
    setHighlightedStates(updatedStates);
  };

  const handleMouseLeave = (index) => {
    const updatedStates = [...highlightedStates];
    updatedStates[index] = false;
    setHighlightedStates(updatedStates);
  };

  return { highlightedStates, handleHover, handleMouseLeave };
};
