export default function Navbar({ state, setState }) {
  return (
    <nav className="fixed top-0 left-0 w-screen flex items-center justify-between px-8 py-4 backdrop-blur-sm z-10">
      <div className="flex items-center space-x-8">
        <div className="text-lg font-semibold text-gray-900">Retool</div>
        <div className="hidden md:flex space-x-7 text-sm">
          <a href="#" className="text-gray-600 hover:text-gray-900">
            Pricing
          </a>
          <a href="#" className="text-gray-600 hover:text-gray-900">
            Templates
          </a>
          <a href="#" className="text-gray-600 hover:text-gray-900">
            Use Cases
          </a>
          <a href="#" className="text-gray-600 hover:text-gray-900">
            Pricing
          </a>
          <a href="#" className="text-gray-600 hover:text-gray-900">
            Docs
          </a>
        </div>
      </div>
      <button className="bg-gray-700 text-white px-4 py-2 rounded-md text-sm hover:bg-gray-800 transition-colors">Login</button>
    </nav>
  );
}
