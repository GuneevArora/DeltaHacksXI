import './styles.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import IconBtn from './IconBtn.tsx';
import PwnCard from './PwnCard.tsx';


ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/icon_btn" element={<IconBtn />} />
                <Route path="/pwn_card" element={<PwnCard />} />
                <Route path="/goggle" element={
                    <div className='w-full h-20 bg-slate-600'>

                    </div>
                } />
            </Routes>
        </BrowserRouter>
    </React.StrictMode>,
    document.getElementById('root')
);
