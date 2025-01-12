import './styles.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import IconBtn from './IconBtn.tsx';
import PwnCard from './PwnCard.tsx';
import PWShower from './PWShower.tsx';
import Vault from './Vault.tsx';


ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/icon_btn" element={<IconBtn />} />
                <Route path="/pwn_card" element={<PwnCard />} />
                <Route path="/pw_shower" element={<PWShower />} />
                <Route path="/vault" element={<Vault />} />
            </Routes>
        </BrowserRouter>
    </React.StrictMode>,
    document.getElementById('root')
);
