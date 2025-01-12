import React, { ReactElement, useEffect, useState } from 'react';
import { ComponentProps, Streamlit, withStreamlitConnection } from 'streamlit-component-lib';


function IconBtn({ args }: ComponentProps): ReactElement {
    const { src } = args;
    const [clicked,setClicked] = useState(false);

    const HEIGHT = 150;
    
    useEffect(() => {
        Streamlit.setFrameHeight(HEIGHT);
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
        <div className="w-full flex justify-center items-center transition transform scale-[95%] hover:scale-[98%]" style={{height: `${HEIGHT}px`}}>
            <button className="flex justify-center items-center w-40 aspect-square border border-2 rounded-lg"  onClick={() => { Streamlit.setComponentValue(1); setClicked(true); }}>
                <img style={{maxWidth: "50%", maxHeight: "50%"}} src={src}>
                </img>
            </button>
        </div>
    )
}

export default withStreamlitConnection(IconBtn);
