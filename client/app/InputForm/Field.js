

function Field(props) {
    return (
        <div className="flex items-center mb-6 w-full">
            <div className="w-1/4">
                <label className="block text-gray-500 font-bold pr-2">
                    {props.title}
                </label>
            </div>
            <div className="w-3/4">
                <input ref={props.inputref} className="bg-gray-200 appearance-none border-2 
                border-gray-200 rounded w-full py-2 px-2 text-gray-700 
                leading-tight" id="inline-full-name" type="text">
                </input>
            </div>
        </div>
    )
}

export default Field;