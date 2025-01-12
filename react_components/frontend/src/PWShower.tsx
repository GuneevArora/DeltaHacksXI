import React, { ReactElement, useEffect, useState } from 'react';
import { ComponentProps, Streamlit, withStreamlitConnection } from 'streamlit-component-lib';

type Entry = {
    site: string,
    username: string
}

type Args = {
    entries: Entry[]
};

function PWShower({ args }: ComponentProps): ReactElement {
    const { entries } = args as Args;
    const [lastClicked,setLastClicked] = useState(-1);

    useEffect(() => {
        Streamlit.setFrameHeight();
    });

    useEffect(() => {
        if (lastClicked != -1) {
            setTimeout(() => {
                Streamlit.setComponentValue(-1);
                setLastClicked(-1);
            }, 1000);
        }
    }, [lastClicked]);

    return (
        <div className="w-full h-full overflow-auto">
            {
                entries.map( (e,i) => (
                    <div className="w-full transform animation cursor-pointer scale-90 hover:scale-100 border p-2 rounded-lg" key={i} onClick={() => { Streamlit.setComponentValue(i); setLastClicked(i); }}>
                        <h2>{ e.site }</h2>
                        <hr></hr>
                        <p><span>User: </span>{ e.username }</p>
                        <p><span>Password: </span>**********</p>
                    </div>
                ))
            }
        </div>
    );
}

export default withStreamlitConnection(PWShower);
