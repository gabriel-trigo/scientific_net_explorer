'use client'
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function InputForm(
    setGraph
) {

    function handleSubmit() {
        axios.get(
            'http://127.0.0.1:8000/erdos/'
        ).then((data) => {
            console.log(data);
        })
    }

    return (
    <div className="border rounded border-gray-300 p-2 w-3/4">
        <div className="flex items-center mb-6 w-full">
            <div className="w-1/4">
                <label className="block text-gray-500 font-bold pr-2">
                Source Author
                </label>
            </div>
            <div className="w-3/4">
                <input className="bg-gray-200 appearance-none border-2 
                border-gray-200 rounded w-full py-2 px-2 text-gray-700 
                leading-tight focus:outline-none focus:bg-white 
                focus:border-purple-500" id="inline-full-name" type="text">
                </input>
            </div>
        </div>
        <div className="flex items-center mb-6 w-full">
            <div className="md:w-1/4">
                <label className="block text-gray-500 font-bold text-left pr-2" for="inline-full-name">
                Target Author
                </label>
            </div>
            <div className="w-3/4">
                <input className="bg-gray-200 appearance-none border-2 
                border-gray-200 rounded w-full py-2 px-2 text-gray-700 
                leading-tight focus:outline-none focus:bg-white 
                focus:border-purple-500" id="inline-full-name" type="text">
                </input>
            </div>
        </div>
        <div className="w-full items-center text-left">
            <button onClick={handleSubmit} className="bg-purple-500 hover:bg-purple-400 
                border-b-4 border-purple-800 px-3 py-1 text-white 
                font-semibold rounded">
                Dark Mode
            </button>
        </div>
    </div>
  );
}

export default InputForm;

