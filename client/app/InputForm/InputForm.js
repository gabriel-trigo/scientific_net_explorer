'use client'
import React, { useRef } from 'react';
import Field from './Field'
import { SnackbarProvider, enqueueSnackbar } from 'notistack'

function InputForm({
    setNodes,
    setEdges,  
    setIsLoading, 
    isLoading, 
    setNumAuthors, 
    setNumPapers
}) {

    // Form references.
    const srcInput = useRef(null);
    const tgtInput = useRef(null);

    async function handleSubmit() {

        if (isLoading) {
            enqueueSnackbar(
                "Please wait for the current search to conclude.", 
                { variant: "warning" }
            );
            return;
        }

        setIsLoading(true); // Start loading.
        setNumAuthors(0);
        setNumPapers(0);

        // Make request to backend.
        const url = new URL('http://127.0.0.1:8000/erdos/');
        url.searchParams.append('src', srcInput.current.value);
        url.searchParams.append('tgt', tgtInput.current.value);
        var response = await fetch(url, { method: 'GET' });

        // Backend couldn't find authors.
        if (response.status != 200) {
            enqueueSnackbar(
                "Couldn't find source/target authors.",
                { variant: "error" });
            cleanup();
            return
        } else {
            enqueueSnackbar(
                "Source/target authors found, initiation search.",
                { variant: "success" }
            )
        }
        
        // Read StreamingResponse.
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let text = "";
        let loadingData; 

        while (true) {

            try {
                var { value, done } = await reader.read(); // Read next chunk
                if (done) { break; }
            } catch(error) {
                cleanup(error);
            }

            text += decoder.decode(value);
            let dictArray = text.split("@");
            try { 
                loadingData = JSON.parse(dictArray[dictArray.length - 1]);
                setNumAuthors(loadingData["num_nodes"]);
                setNumPapers(loadingData["num_papers"]);
            } catch(error) { continue; } // In case chunk is not full dict.
        }
        setNodes(loadingData["nodes"].map((e) => JSON.parse(e)));
        setEdges(loadingData["edges"].map((e) => {
            return {
                "source": JSON.parse(e["source"]), 
                "target": JSON.parse(e["target"])
            }}));
        setIsLoading(false); // Done loading.
    }

    function cleanup() {
        setIsLoading(false);
        setNumAuthors(null);
    }

    return (
        <div className="border rounded border-gray-300 p-2 w-3/4">
            <Field 
                inputref={ srcInput }
                title={ "Source Author" }
            />
            <Field 
                inputref={ tgtInput }
                title={ "Target Author" }
            />
            <div className="w-full items-center text-left">
                <button onClick={ handleSubmit } className="bg-purple-500 
                    hover:bg-purple-400 px-3 py-1 text-white 
                    font-semibold rounded">
                    Submit
                </button>
            </div>
        </div>
    );
}

export default InputForm;

