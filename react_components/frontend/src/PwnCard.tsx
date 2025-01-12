import {
    Streamlit,
    withStreamlitConnection,
    ComponentProps,
  } from "streamlit-component-lib"
  import React, { useCallback, useEffect, useMemo, useState, ReactElement } from "react"
  
  /**
   * This is a React-based component template. The passed props are coming from the 
   * Streamlit library. Your custom args can be accessed via the `args` props.
   */
  function PwnCard({ args, disabled, theme }: ComponentProps): ReactElement {
    const { header, body } = args;
    const [clicked,setClicked] = useState(false);
  
    useEffect(() => {
            Streamlit.setFrameHeight();
        });
    
    useEffect(() => {
            if (clicked) {
                setTimeout(() => {
                    Streamlit.setComponentValue(0);
                    setClicked(false);
                }, 1000);
            }
        }, [clicked]);
  
    return (
      <div className="bg-neutral-800 p-10 rounded-md border border-neutral-300 hover:shadow-xl transition-transform scale-95 origin-center hover:scale-[97%]">
          <h5 className="m-1 font-bold text-xl">{header}</h5>
          <p className="m-1 w-[80px] text-wrap">{body}</p>
        <button onClick={() => { Streamlit.setComponentValue(1); setClicked(true); }}type="button" className="m-2 p-1 rounded-md w-full bg-red-500 shadow-sm hover:scale-[101%] hover:bg-red-400 active:bg-red-600 ">Inspect Threat</button>
      </div>
    )
  }
  
  // "withStreamlitConnection" is a wrapper function. It bootstraps the
  // connection between your component and the Streamlit app, and handles
  // passing arguments from Python -> Component.
  //
  // You don't need to edit withStreamlitConnection (but you're welcome to!).
  export default withStreamlitConnection(PwnCard)