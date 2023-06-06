using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Models
{
    public class Angulos
    {
        public int Id { get; set; }
        public int A11 { get; set; }
        public int A12 { get; set; }
        public int A21 { get; set; }
        public int A22 { get; set; }
        public int A31 { get; set; }
        public int A32 { get; set; }
        public int A41 { get; set; }
        public int A42 { get; set; }
        public DateTime? Fecha { get; set; }
    }
}
