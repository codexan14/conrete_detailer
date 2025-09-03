function MyButton() {
    return (
        <button> I'm a button </button>
    ); 
}

export default function MyApp() {
    return (
        <div>
            <h1>My Welcome Page</h1>
            <MyButton />
        </div>
    );
}