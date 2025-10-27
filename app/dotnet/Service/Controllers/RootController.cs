using Microsoft.AspNetCore.Mvc;
using System.Runtime.InteropServices;

namespace Service.Controllers;

// Example of an action directly at the root of the API
[ApiController]
public class RootController : ControllerBase
{
    // GET / (root of the API)
    [HttpGet("/")]
    public ContentResult GetRootMessage()
    {
        string frameworkDescription = RuntimeInformation.FrameworkDescription;
        string jsonString = $"{{'Server':'.NET Server', 'Version':'{frameworkDescription}'}}";
        return Content(jsonString, "application/json");
    }
}
