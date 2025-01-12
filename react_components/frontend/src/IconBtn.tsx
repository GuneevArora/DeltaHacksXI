import React, { ReactElement, useEffect, useState } from 'react';
import { ComponentProps, Streamlit, withStreamlitConnection } from 'streamlit-component-lib';


function IconBtn({ args }: ComponentProps): ReactElement {
    const { src } = args;
    const [clicked,setClicked] = useState(false);
    
    useEffect(() => {
        Streamlit.setFrameHeight(100);
    });

    useEffect(() => {
        if (clicked) {
            Streamlit.setComponentValue(false);
            setClicked(false);
        }
    }, [clicked]);

    return (
        <button style={{width: "50px", height: "50px"}} onClick={() => { Streamlit.setComponentValue(true); setClicked(true); }}>
            <img style={{maxWidth: "90%", maxHeight: "90%"}} src={src}>
            </img>
        </button>
    )
}

export default withStreamlitConnection(IconBtn);
