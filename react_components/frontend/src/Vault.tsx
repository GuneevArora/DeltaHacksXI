import React, { ReactElement, useEffect, useState } from 'react';
import { ComponentProps, Streamlit, withStreamlitConnection } from 'streamlit-component-lib';

type Args = {
    files: string[]
};

type Action = {
    deleteMode: boolean,
    file: string,
    idx: number
};

function Vault({ args }: ComponentProps): ReactElement {
    const { files } = args as Args;
    const [action,setAction] = useState<Action | null>(null);

    console.log(files);

    useEffect(() => {
        Streamlit.setFrameHeight();
    });

    useEffect(() => {
        if (action !== null) {
            setTimeout(() => {
                Streamlit.setComponentValue(null);
                setAction(null);
            }, 1000);
        }
    }, [action]);

    return (
        <div className="w-full h-full overflow-auto">
            {
                files.map( (f,i) => (
                    <div className="w-full h-32 p-4 border-2 rounded-lg" key={i}>
                        <div className="flex h-full items-center flex-row justify-between">
                            <h3>{ f }</h3>
                            <div className="h-full flex flex-col justify-evenly">
                                <button className="p-2 hover:bg-purple-500 rounded-md bg-purple-300"
                                    onClick={() => {
                                        const action: Action = { deleteMode: true, file: f, idx: i };
                                        Streamlit.setComponentValue(action);
                                        setAction(action);
                                    }}
                                    >
                                    Delete
                                </button>

                                <button className="p-2 hover:bg-purple-500 rounded-md bg-purple-300"
                                    onClick={() => {
                                        const action: Action = { deleteMode: false, file: f, idx: i };
                                        Streamlit.setComponentValue(action);
                                        setAction(action);
                                    }}
                                    >
                                    Extract
                                </button>
                            </div>
                        </div>
                    </div>
                ))
            }
        </div>
    );
}

export default withStreamlitConnection(Vault);
